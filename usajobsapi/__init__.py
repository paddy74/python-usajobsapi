"""Top-level package for the USAJOBS REST API wrapper."""

from usajobsapi._version import __license__, __title__
from usajobsapi.client import USAJobsClient

__all__: list[str] = ["__license__", "__title__", "USAJobsClient"]
