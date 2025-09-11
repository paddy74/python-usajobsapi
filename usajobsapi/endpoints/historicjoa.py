"""Wrapper for the Historic JOAs API."""

from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

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

        model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)

        hiring_agency_codes: Optional[str] = Field(
            None, serialization_alias="HiringAgencyCodes"
        )
        hiring_department_codes: Optional[str] = Field(
            None, serialization_alias="HiringDepartmentCodes"
        )
        position_series: Optional[str] = Field(
            None, serialization_alias="PositionSeries"
        )
        announcement_numbers: Optional[str] = Field(
            None, serialization_alias="AnnouncementNumbers"
        )
        usajobs_control_numbers: Optional[str] = Field(
            None, serialization_alias="USAJOBSControlNumbers"
        )
        start_position_open_date: Optional[str] = Field(
            None, serialization_alias="StartPositionOpenDate"
        )  # YYYY-MM-DD
        end_position_open_date: Optional[str] = Field(
            None, serialization_alias="EndPositionOpenDate"
        )
        start_position_close_date: Optional[str] = Field(
            None, serialization_alias="StartPositionCloseDate"
        )
        end_position_close_date: Optional[str] = Field(
            None, serialization_alias="EndPositionCloseDate"
        )
        continuation_token: Optional[str] = Field(
            None, serialization_alias="continuationtoken"
        )

        def to_params(self) -> Dict[str, str]:
            return _dump_by_alias(self)

    class Response(BaseModel):
        """Declarative definition for the endpoint's response object."""

        pass
