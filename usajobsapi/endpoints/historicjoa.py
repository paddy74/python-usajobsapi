"""Wrapper for the Historic JOAs API."""

from typing import Dict

from pydantic import BaseModel

from usajobsapi.utils import _dump_by_alias


class HistoricJoaEndpoint(BaseModel):
    """
    Declarative endpoint definition for the [Historic JOAs API](https://developer.usajobs.gov/api-reference/get-api-historicjoa).

    Includes the endpoint's:

    - Parameters
    - Response shapes
    - Metadata
    """

    METHOD: str = "GET"
    PATH: str = "/api/historicjoa"

    class Params(BaseModel):
        """Declarative definition for the endpoint's query parameters."""

        def to_params(self) -> Dict[str, str]:
            return _dump_by_alias(self)

    class Response(BaseModel):
        """Declarative definition for the endpoint's response object."""

        pass
