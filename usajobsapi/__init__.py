"""Top-level package for the USAJOBS REST API wrapper."""

from usajobsapi._version import __license__, __title__
from usajobsapi.client import USAJobsApiClient

__all__: list[str] = ["__license__", "__title__", "USAJobsApiClient"]
