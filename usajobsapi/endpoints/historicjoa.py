"""Wrapper for the Historic JOAs API."""

import datetime as dt
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from usajobsapi.utils import _dump_by_alias, _normalize_date


class HistoricJoaEndpoint(BaseModel):
    """
    Declarative wrapper around the [Historic JOAs API](https://developer.usajobs.gov/api-reference/get-api-historicjoa).
    """

    METHOD: str = "GET"
    PATH: str = "/api/historicjoa"

    class Params(BaseModel):
        """Declarative definition of the endpoint's query parameters."""

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
        start_position_open_date: Optional[dt.date] = Field(
            default=None, serialization_alias="StartPositionOpenDate"
        )
        end_position_open_date: Optional[dt.date] = Field(
            default=None, serialization_alias="EndPositionOpenDate"
        )
        start_position_close_date: Optional[dt.date] = Field(
            default=None, serialization_alias="StartPositionCloseDate"
        )
        end_position_close_date: Optional[dt.date] = Field(
            default=None, serialization_alias="EndPositionCloseDate"
        )
        continuation_token: Optional[str] = Field(
            None, serialization_alias="continuationtoken"
        )

        def to_params(self) -> Dict[str, str]:
            """Serialize params into payload-ready query parameters."""
            return _dump_by_alias(self)

        @field_validator(
            "start_position_open_date",
            "end_position_open_date",
            "start_position_close_date",
            "end_position_close_date",
            mode="before",
        )
        @classmethod
        def _normalize_date_fields(
            cls, value: None | dt.datetime | dt.date | str
        ) -> Optional[dt.date]:
            """Coerce date-like inputs to `datetime.date`."""

            return _normalize_date(value)

    # Response shapes
    # ---

    class Item(BaseModel):
        """A single historic job opportunity announcement record."""

        usajobs_control_number: int = Field(alias="usajobsControlNumber")
        position_title: Optional[str] = Field(default=None, alias="positionTitle")
        hiring_agency_code: Optional[str] = Field(
            default=None, alias="hiringAgencyCode"
        )
        hiring_department_code: Optional[str] = Field(
            default=None, alias="hiringDepartmentCode"
        )
        position_open_date: Optional[str] = Field(
            default=None, alias="positionOpenDate"
        )
        position_close_date: Optional[str] = Field(
            default=None, alias="positionCloseDate"
        )
        minimum_salary: Optional[float] = Field(default=None, alias="minimumSalary")
        maximum_salary: Optional[float] = Field(default=None, alias="maximumSalary")

    class PagingMeta(BaseModel):
        """Pagination metadata returned alongside Historic JOA results."""

        total_count: Optional[int] = Field(default=None, alias="totalCount")
        page_size: Optional[int] = Field(default=None, alias="pageSize")
        continuation_token: Optional[str] = Field(
            default=None, alias="continuationToken"
        )

    class Paging(BaseModel):
        """Container for pagination metadata and optional navigation links."""

        metadata: "HistoricJoaEndpoint.PagingMeta"
        next: Optional[str] = None

    class Response(BaseModel):
        """Declarative definition of the endpoint's response object."""

        paging: Optional["HistoricJoaEndpoint.Paging"] = None
        data: List["HistoricJoaEndpoint.Item"] = Field(default_factory=list)

        def next_token(self) -> Optional[str]:
            """Return the continuation token for requesting the next page."""

            return (
                self.paging.metadata.continuation_token
                if self.paging and self.paging.metadata
                else None
            )
