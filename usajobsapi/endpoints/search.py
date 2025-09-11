"""Wrapper for the Job Search API."""

from enum import StrEnum
from typing import Dict

from pydantic import BaseModel

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
    """Declarative endpoint definition for the Job Search API."""

    method: str = "GET"
    path: str = "/api/search"

    class Params(BaseModel):
        def to_params(self) -> Dict[str, str]:
            return _dump_by_alias(self)

    class Response(BaseModel):
        pass
