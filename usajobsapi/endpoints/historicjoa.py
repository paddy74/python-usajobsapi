"""Wrapper for the Historic JOAs API."""

from typing import Dict

from pydantic import BaseModel

from usajobsapi.utils import _dump_by_alias


class HistoricJoaEndpoint(BaseModel):
    method: str = "GET"
    path: str = "/api/historicjoa"

    class Params(BaseModel):
        def to_params(self) -> Dict[str, str]:
            return _dump_by_alias(self)

    class Response(BaseModel):
        pass
