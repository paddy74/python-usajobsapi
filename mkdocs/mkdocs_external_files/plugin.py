# plugins/external_files.py
import hashlib
import logging
import shutil
from glob import glob
from pathlib import Path
from typing import Any, Callable

from mkdocs.config import config_options as c
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.livereload import LiveReloadServer
from mkdocs.plugins import BasePlugin

logger = logging.getLogger(__name__)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


class ExternalFilesPlugin(BasePlugin):
    """
    Copy files that live outside docs_dir into docs_dir before the build.

    Config:
      * Relative src paths resolve against the MkDocs config directory.
      files:
        - src: README.md              # file
          dest: external/README.md
        - src: LICENSE                # file -> rename/relocate
          dest: external/LICENSE.txt
        - src: assets/**              # glob (copies all matches)
          dest: external/assets/      # must end with '/' to indicate a directory
    """

    config_scheme = (
        ("files", c.Type(list, default=[])),  # list of {src: str, dest: str}
    )

    def on_config(self, config):
        self.docs_dir = Path(config["docs_dir"]).resolve()

        config_path = getattr(config, "config_file_path", None)
        if config_path:
            self.config_dir = Path(config_path).resolve().parent
        else:
            self.config_dir = Path.cwd()

        logger.debug(
            "external-files: docs_dir=%s config_dir=%s", self.docs_dir, self.config_dir
        )

        return config

    def _copy_file(self, src: Path, dest: Path):
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            try:
                if _sha256(src) == _sha256(dest):
                    logger.debug("external-files: skip identical %s", dest)
                    return  # identical; skip
            except Exception:
                pass
        logger.debug("external-files: copy %s -> %s", src, dest)
        shutil.copy2(src, dest)

    def _expand_items(self):
        """
        Yields (src_path, dest_path) pairs. Supports:
          - single file -> file
          - glob -> directory (dest must end with '/')
        """
        for item in self.config["files"]:
            src = item["src"]
            dest = item["dest"]
            if any(ch in src for ch in ["*", "?", "["]):
                # glob mode: dest must be a directory (end with '/')
                if not dest.endswith(("/", "\\")):
                    raise ValueError(
                        f"When using glob in src='{src}', dest must be a directory (end with '/')."
                    )
                pattern = src
                if not Path(pattern).is_absolute():
                    pattern = str((self.config_dir / pattern).resolve())
                matched = [Path(p).resolve() for p in glob(pattern, recursive=True)]
                for s in matched:
                    if s.is_file():
                        rel_name = s.name
                        yield s, (self.docs_dir / dest / rel_name).resolve()
            else:
                s = Path(src)
                if not s.is_absolute():
                    s = self.config_dir / s
                s = s.resolve()
                d = (self.docs_dir / dest).resolve()
                yield s, d

    def on_pre_build(self, *, config: MkDocsConfig) -> None:
        copied = 0
        for src, dest in self._expand_items():
            if not src.exists():
                raise FileNotFoundError(f"external-files: source not found: {src}")
            self._copy_file(src, dest)
            copied += 1
        logger.debug("external-files: staged %s file(s) into %s", copied, self.docs_dir)

    # Make mkdocs serve auto-reload when source files change
    def on_serve(
        self,
        server: LiveReloadServer,
        /,
        *,
        config: MkDocsConfig,
        builder: Callable[..., Any],
    ) -> LiveReloadServer | None:
        try:
            for src, _ in self._expand_items():
                if src.exists():
                    server.watch(str(src))
        except Exception:
            pass
        return server
