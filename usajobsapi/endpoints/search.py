"""Wrapper for the Job Search API."""

from enum import StrEnum
from typing import Annotated, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from usajobsapi.utils import _dump_by_alias

# Enums for query-params
# ---


class SortField(StrEnum):
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
    ASC = "Asc"
    DESC = "Desc"


class WhoMayApply(StrEnum):
    ALL = "All"
    PUBLIC = "Public"
    STATUS = "Status"


class Fields(StrEnum):
    MIN = "Min"
    FULL = "Full"


class HiringPath(StrEnum):
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
    Declarative endpoint definition for the Job Search API.

    Includes the endpoint's:

    - Parameters
    - Response shapes
    - Metadata
    """

    method: str = "GET"
    path: str = "/api/search"

    class Params(BaseModel):
        """Declarative query-parameter model"""

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

        def to_params(self) -> Dict[str, str]:
            return _dump_by_alias(self)

    # Response shapes
    # ---
    class JobSummary(BaseModel):
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

    class Response(BaseModel):
        pass
