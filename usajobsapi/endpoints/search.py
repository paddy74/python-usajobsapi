"""Wrapper for the Job Search API."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Any, Dict, List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
    model_validator,
)

from usajobsapi.utils import _dump_by_alias

# Enums for query-params
# ---


class SortField(StrEnum):
    """Sort the search by the specified field."""

    OPEN_DATE = "opendate"
    CLOSED_DATE = "closedate"
    ORGANIZATION_NAME = "organizationname"
    JOB_TITLE = "jobtitle"
    POSITION_TITLE = "positiontitle"
    OPENING_DATE = "openingdate"
    CLOSING_DATE = "closingdate"
    HO_NAME = "honame"
    SALARY_MIN = "salarymin"
    LOCATION = "location"
    DEPARTMENT = "department"
    TITLE = "title"
    AGENCY = "agency"
    SALARY = "salary"


class SortDirection(StrEnum):
    """Sort the search by the SortField specified, in the direction specified."""

    ASC = "Asc"
    DESC = "Desc"


class WhoMayApply(StrEnum):
    """Filter the search by the specified candidate designation."""

    ALL = "All"
    PUBLIC = "Public"
    STATUS = "Status"


class Fields(StrEnum):
    """Return the minimum or maximum number of fields for each result item."""

    MIN = "Min"  # Return only the job summary
    FULL = "Full"


class HiringPath(StrEnum):
    """Filter search results by the specified hiring path(s)."""

    PUBLIC = "public"
    VET = "vet"
    N_GUARD = "nguard"
    DISABILITY = "disability"
    NATIVE = "native"
    M_SPOUSE = "mspouse"
    STUDENT = "student"
    SES = "ses"
    PEACE = "peace"
    OVERSEAS = "overseas"
    FED_INTERNAL_SEARCH = "fed-internal-search"
    GRADUATES = "graduates"
    FED_EXCEPTED = "fed-excepted"
    FED_COMPETITIVE = "fed-competitive"
    FED_TRANSITION = "fed-transition"
    LAND = "land"
    SPECIAL_AUTHORITIES = "special-authorities"


# Endpoint declaration
# ---
class SearchEndpoint(BaseModel):
    """
    Declarative wrapper around the [Job Search API](https://developer.usajobs.gov/api-reference/get-api-search).
    """

    METHOD: str = "GET"
    PATH: str = "/api/search"

    class Params(BaseModel):
        """Declarative definition of the endpoint's query parameters."""

        model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)

        keyword: Optional[str] = Field(None, serialization_alias="Keyword")
        position_title: Optional[str] = Field(None, serialization_alias="PositionTitle")

        remuneration_min: Optional[int] = Field(
            None, serialization_alias="RemunerationMinimumAmount"
        )
        remuneration_max: Optional[int] = Field(
            None, serialization_alias="RemunerationMaximumAmount"
        )
        pay_grade_high: Optional[str] = Field(None, serialization_alias="PayGradeHigh")
        pay_grade_low: Optional[str] = Field(None, serialization_alias="PayGradeLow")

        job_category_codes: List[str] = Field(
            default_factory=list, serialization_alias="JobCategoryCode"
        )
        position_schedule_type_codes: List[str] = Field(
            default_factory=list, serialization_alias="PositionScheduleTypeCode"
        )
        position_offering_type_codes: List[str] = Field(
            default_factory=list, serialization_alias="PositionOfferingTypeCode"
        )

        organization: List[str] = Field(
            default_factory=list, serialization_alias="Organization"
        )
        location_names: List[str] = Field(
            default_factory=list, serialization_alias="LocationName"
        )
        radius: Annotated[
            Optional[int], Field(serialization_alias="Radius", strict=True, gt=0)
        ] = None

        travel_percentage: List[str] = Field(
            default_factory=list, serialization_alias="TravelPercentage"
        )
        relocation: Optional[bool] = Field(
            None, serialization_alias="RelocationIndicator"
        )
        security_clearance_required: List[str] = Field(
            default_factory=list, serialization_alias="SecurityClearanceRequired"
        )
        position_sensitivity: List[str] = Field(
            default_factory=list, serialization_alias="PositionSensitivity"
        )

        who_may_apply: Optional[WhoMayApply] = Field(
            None, serialization_alias="WhoMayApply"
        )
        hiring_paths: List[HiringPath] = Field(
            default_factory=list, serialization_alias="HiringPath"
        )

        salary_bucket: List[str] = Field(
            default_factory=list, serialization_alias="SalaryBucket"
        )
        grade_bucket: List[str] = Field(
            default_factory=list, serialization_alias="GradeBucket"
        )

        supervisory_status: Optional[str] = Field(
            None, serialization_alias="SupervisoryStatus"
        )
        date_posted_days: Annotated[
            Optional[int],
            Field(serialization_alias="DatePosted", strict=True, ge=0, le=60),
        ] = None
        job_grade_codes: List[str] = Field(
            default_factory=list, serialization_alias="JobGradeCode"
        )
        mission_critical_tags: List[str] = Field(
            default_factory=list, serialization_alias="MissionCriticalTags"
        )

        sort_field: Optional[SortField] = Field(None, serialization_alias="SortField")
        sort_direction: Optional[SortDirection] = Field(
            None, serialization_alias="SortDirection"
        )
        page: Annotated[
            Optional[int], Field(serialization_alias="Page", strict=True, ge=1)
        ] = None
        results_per_page: Annotated[
            Optional[int],
            Field(serialization_alias="ResultsPerPage", strict=True, ge=1, le=500),
        ] = None
        fields: Optional[Fields] = Field(None, serialization_alias="Fields")

        remote_indicator: Optional[bool] = Field(
            None, serialization_alias="RemoteIndicator"
        )

        @model_validator(mode="after")
        def _radius_requires_location(self) -> "SearchEndpoint.Params":
            """Only use radius filters when a locaiton is provided."""
            if self.radius is not None and not self.location_names:
                raise ValueError("Radius requires at least one LocationName.")
            return self

        @field_validator("remuneration_max")
        @classmethod
        def _check_min_le_max(
            cls, v: Optional[int], info: ValidationInfo
        ) -> Optional[int]:
            """Validate that renumeration max is >= renumeration min."""
            mn = info.data.get("remuneration_min")
            if v is not None and mn is not None and v < mn:
                raise ValueError(
                    "RemunerationMaximumAmount must be >= RemunerationMinimumAmount."
                )
            return v

        def to_params(self) -> Dict[str, str]:
            """Return the serialized query-parameter dictionary."""
            return _dump_by_alias(self)

    # Response shapes
    # ---

    class JobSummary(BaseModel):
        """Normalized representation of a search result item."""

        id: str = Field(alias="MatchedObjectId")
        position_title: str = Field(alias="PositionTitle")
        organization_name: Optional[str] = Field(default=None, alias="OrganizationName")
        locations_display: Optional[str] = Field(
            default=None, alias="PositionLocationDisplay"
        )
        min_salary: Optional[float] = Field(default=None, alias="MinimumRange")
        max_salary: Optional[float] = Field(default=None, alias="MaximumRange")
        application_close_date: Optional[str] = Field(
            default=None, alias="ApplicationCloseDate"
        )

    class SearchResult(BaseModel):
        """Model of paginated search results."""

        result_count: Optional[int] = Field(
            default=None,
            alias="SearchResultCount",
        )
        result_total: Optional[int] = Field(
            default=None,
            alias="SearchResultCountAll",
        )
        items: List[Dict[str, Any]] = Field(
            default_factory=list,
            alias="SearchResultItems",
        )

        def jobs(self) -> List[SearchEndpoint.JobSummary]:
            """Normalize the list of search results, skiping malformed payloads."""
            out: List[SearchEndpoint.JobSummary] = []
            for item in self.items:
                # Some responses nest the item under 'MatchedObjectDescriptor'
                descriptor = item.get("MatchedObjectDescriptor") or item
                try:
                    out.append(SearchEndpoint.JobSummary.model_validate(descriptor))
                except ValidationError:
                    continue
            return out

    class Response(BaseModel):
        """Declarative definition of the endpoint's response object."""

        language: Optional[str] = Field(default=None, alias="LanguageCode")
        params: Optional[SearchEndpoint.Params] = Field(
            default=None, alias="SearchParameters"
        )
        # Results are wrapped under SearchResult
        search_result: Optional[SearchEndpoint.SearchResult] = Field(
            default=None, alias="SearchResult"
        )
