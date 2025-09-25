from mkdocs.config.defaults import MkDocsConfig
from usajobsapi import _version as md


def on_config(config: MkDocsConfig):
    config.site_name = f"{md.__title__} {md.__version__}"
    config.site_author = md.__author__

    return config
