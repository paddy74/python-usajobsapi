"""Wrapper for USAJOBS REST API endpoints."""

from announcementtext import AnnouncementTextEndpoint
from historicjoa import HistoricJoaEndpoint
from search import SearchEndpoint

__all__: list[str] = [
    "AnnouncementTextEndpoint",
    "HistoricJoaEndpoint",
    "SearchEndpoint",
]
