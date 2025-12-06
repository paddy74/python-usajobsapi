"""
Wrapper for the Historic JOAs API.

Access archived job opportunity announcements with date filters, control numbers, and hiring-organization metadata.

- Feed a control number captured from a [search result item's `id`][usajobsapi.endpoints.search.SearchEndpoint.JOAItem] into [`usajobs_control_numbers`][usajobsapi.endpoints.historicjoa.HistoricJoaEndpoint.Params] to retrieve historical records for the same posting.
- Date filters such as [`start_position_open_date`][usajobsapi.endpoints.historicjoa.HistoricJoaEndpoint.Params] normalize strings as `datetime.date` objects and are reflected back in a response's `position_open_date`.
- Boolean indicators rely on normalization validators to handle the API's inconsistent input/output formats for booleans.
"""

import datetime as dt

from pydantic import BaseModel, ConfigDict, Field, field_validator

from usajobsapi.utils import _dump_by_alias, _normalize_date, _normalize_yn_bool


class HistoricJoaEndpoint(BaseModel):
    """
    Declarative wrapper around the [Historic JOAs API](https://developer.usajobs.gov/api-reference/get-api-historicjoa).
    """

    METHOD: str = "GET"
    PATH: str = "/api/historicjoa"

    class Params(BaseModel):
        """Declarative definition of the endpoint's query parameters."""

        model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)

        hiring_agency_codes: str | None = Field(
            None, serialization_alias="HiringAgencyCodes"
        )
        hiring_department_codes: str | None = Field(
            None, serialization_alias="HiringDepartmentCodes"
        )
        position_series: str | None = Field(None, serialization_alias="PositionSeries")
        announcement_numbers: str | None = Field(
            None, serialization_alias="AnnouncementNumbers"
        )
        usajobs_control_numbers: str | None = Field(
            None, serialization_alias="USAJOBSControlNumbers"
        )
        start_position_open_date: dt.date | None = Field(
            default=None, serialization_alias="StartPositionOpenDate"
        )
        end_position_open_date: dt.date | None = Field(
            default=None, serialization_alias="EndPositionOpenDate"
        )
        start_position_close_date: dt.date | None = Field(
            default=None, serialization_alias="StartPositionCloseDate"
        )
        end_position_close_date: dt.date | None = Field(
            default=None, serialization_alias="EndPositionCloseDate"
        )
        continuation_token: str | None = Field(
            None, serialization_alias="continuationToken"
        )

        def to_params(self) -> dict[str, str]:
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
        ) -> dt.date | None:
            """Coerce date-like inputs to `datetime.date`."""

            return _normalize_date(value)

    # Response shapes
    # ---

    class Item(BaseModel):
        """A single historic job opportunity announcement record."""

        class HiringPath(BaseModel):
            hiring_path: str | None = Field(default=None, alias="hiringPath")

        class JobCategory(BaseModel):
            series: str | None = Field(default=None, alias="series")

        class PositionLocation(BaseModel):
            position_location_city: str | None = Field(
                default=None, alias="positionLocationCity"
            )
            position_location_state: str | None = Field(
                default=None, alias="positionLocationState"
            )
            position_location_country: str | None = Field(
                default=None, alias="positionLocationCountry"
            )

        usajobs_control_number: int = Field(alias="usajobsControlNumber")
        hiring_agency_code: str | None = Field(default=None, alias="hiringAgencyCode")
        hiring_agency_name: str | None = Field(default=None, alias="hiringAgencyName")
        hiring_department_code: str | None = Field(
            default=None, alias="hiringDepartmentCode"
        )
        hiring_department_name: str | None = Field(
            default=None, alias="hiringDepartmentName"
        )
        agency_level: int | None = Field(default=None, alias="agencyLevel")
        agency_level_sort: str | None = Field(default=None, alias="agencyLevelSort")
        appointment_type: str | None = Field(default=None, alias="appointmentType")
        work_schedule: str | None = Field(default=None, alias="workSchedule")
        pay_scale: str | None = Field(default=None, alias="payScale")
        salary_type: str | None = Field(default=None, alias="salaryType")
        vendor: str | None = Field(default=None, alias="vendor")
        travel_requirement: str | None = Field(default=None, alias="travelRequirement")
        telework_eligible: bool | None = Field(default=None, alias="teleworkEligible")
        service_type: str | None = Field(default=None, alias="serviceType")
        security_clearance_required: bool | None = Field(
            default=None, alias="securityClearanceRequired"
        )
        security_clearance: str | None = Field(default=None, alias="securityClearance")
        who_may_apply: str | None = Field(default=None, alias="whoMayApply")
        announcement_closing_type_code: str | None = Field(
            default=None, alias="announcementClosingTypeCode"
        )
        announcement_closing_type_description: str | None = Field(
            default=None, alias="announcementClosingTypeDescription"
        )
        position_open_date: dt.date | None = Field(
            default=None, alias="positionOpenDate"
        )
        position_close_date: dt.date | None = Field(
            default=None, alias="positionCloseDate"
        )
        position_expire_date: dt.date | None = Field(
            default=None, alias="positionExpireDate"
        )
        announcement_number: str | None = Field(
            default=None, alias="announcementNumber"
        )
        hiring_subelement_name: str | None = Field(
            default=None, alias="hiringSubelementName"
        )
        position_title: str | None = Field(default=None, alias="positionTitle")
        minimum_grade: str | None = Field(default=None, alias="minimumGrade")
        maximum_grade: str | None = Field(default=None, alias="maximumGrade")
        promotion_potential: str | None = Field(
            default=None, alias="promotionPotential"
        )
        minimum_salary: float | None = Field(default=None, alias="minimumSalary")
        maximum_salary: float | None = Field(default=None, alias="maximumSalary")
        supervisory_status: bool | None = Field(default=None, alias="supervisoryStatus")
        drug_test_required: bool | None = Field(default=None, alias="drugTestRequired")
        relocation_expenses_reimbursed: bool | None = Field(
            default=None, alias="relocationExpensesReimbursed"
        )
        total_openings: str | None = Field(default=None, alias="totalOpenings")
        disable_apply_online: bool | None = Field(
            default=None, alias="disableApplyOnline"
        )
        position_opening_status: str | None = Field(
            default=None, alias="positionOpeningStatus"
        )
        hiring_paths: list["HistoricJoaEndpoint.Item.HiringPath"] = Field(
            default_factory=list, alias="hiringPaths"
        )
        job_categories: list["HistoricJoaEndpoint.Item.JobCategory"] = Field(
            default_factory=list, alias="jobCategories"
        )
        position_locations: list["HistoricJoaEndpoint.Item.PositionLocation"] = Field(
            default_factory=list, alias="positionLocations"
        )

        @field_validator(
            "telework_eligible",
            "security_clearance_required",
            "supervisory_status",
            "drug_test_required",
            "relocation_expenses_reimbursed",
            "disable_apply_online",
            mode="before",
        )
        @classmethod
        def _normalize_yn_boolean(cls, value: None | bool | str) -> bool | None:
            """Coerce bool-like outputs to `bool`."""

            return _normalize_yn_bool(value)

    class PagingMeta(BaseModel):
        """Pagination metadata returned alongside Historic JOA results."""

        total_count: int | None = Field(default=None, alias="totalCount")
        page_size: int | None = Field(default=None, alias="pageSize")
        continuation_token: str | None = Field(default=None, alias="continuationToken")

    class Paging(BaseModel):
        """Container for pagination metadata and optional navigation links."""

        metadata: "HistoricJoaEndpoint.PagingMeta"
        next: str | None = None

    class Response(BaseModel):
        """Declarative definition of the endpoint's response object."""

        paging: "HistoricJoaEndpoint.Paging | None" = None
        data: list["HistoricJoaEndpoint.Item"] = Field(default_factory=list)

        def next_token(self) -> str | None:
            """Return the continuation token for requesting the next page."""

            return (
                self.paging.metadata.continuation_token
                if self.paging and self.paging.metadata
                else None
            )
