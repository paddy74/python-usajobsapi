"""Generate the code reference pages."""

import logging
from pathlib import Path

import mkdocs_gen_files

logger = logging.getLogger(__name__)


def gen_ref_pages(root_dir: Path, source_dir: Path, output_dir: str | Path) -> None:
    """Emit mkdocstrings-compatible reference pages and navigation entries."""
    nav = mkdocs_gen_files.Nav()
    output_dir = Path(output_dir)

    for path in sorted(source_dir.rglob("*.py")):
        module_path = path.relative_to(source_dir).with_suffix("")
        doc_path = path.relative_to(source_dir).with_suffix(".md")
        full_doc_path = output_dir / doc_path

        module_parts = module_path.parts

        if module_parts[-1] == "__main__":
            logger.debug("skip __main__ module: %s", path)
            continue
        if module_parts[-1] == "__init__":
            module_parts = module_parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")

        full_parts = (source_dir.name,) + module_parts
        nav[full_parts] = doc_path.as_posix()

        if not module_parts:
            identifier = source_dir.name
        else:
            identifier = ".".join(full_parts)

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            print("::: " + identifier, file=fd)
        logger.debug("generated doc for %s -> %s", identifier, full_doc_path)

        mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root_dir))

    with mkdocs_gen_files.open("ref/NAV_REF.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


root = Path(__file__).parent.parent
src = root / "usajobsapi"
gen_ref_pages(root, src, "ref")
