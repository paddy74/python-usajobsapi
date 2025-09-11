"""Wrapper for the Announcement Text API."""

from typing import Dict

from pydantic import BaseModel

from usajobsapi.utils import _dump_by_alias


class AnnouncementTextEndpoint(BaseModel):
    method: str = "GET"
    path: str = "/api/historicjoa/announcementtext"

    class Params(BaseModel):
        def to_params(self) -> Dict[str, str]:
            return _dump_by_alias(self)

    class Response(BaseModel):
        pass
