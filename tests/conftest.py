from typing import Dict, List

import pytest


@pytest.fixture
def historicjoa_params_kwargs() -> Dict[str, str]:
    """Field-value mapping used to build HistoricJoaEndpoint params models."""

    return {
        "hiring_agency_codes": "AGENCY1",
        "hiring_department_codes": "DEPT1",
        "position_series": "2210",
        "announcement_numbers": "23-ABC",
        "usajobs_control_numbers": "1234567",
        "start_position_open_date": "2020-01-01",
        "end_position_open_date": "2020-12-31",
        "start_position_close_date": "2021-01-01",
        "end_position_close_date": "2021-12-31",
        "continuation_token": "token123",
    }


@pytest.fixture
def historicjoa_response_payload() -> Dict[str, object]:
    """Serialized Historic JOA response payload mimicking the USAJOBS API."""

    return {
        "paging": {
            "metadata": {
                "totalCount": 2,
                "pageSize": 2,
                "continuationToken": "NEXTTOKEN",
            },
            "next": "https://example.invalid/historicjoa?page=2",
        },
        "data": _historicjoa_items(),
    }


def _historicjoa_items() -> List[Dict[str, object]]:
    return [
        {
            "usajobsControlNumber": 123456789,
            "hiringAgencyCode": "NASA",
            "hiringAgencyName": "National Aeronautics and Space Administration",
            "hiringDepartmentCode": "NAT",
            "hiringDepartmentName": "Department of Science",
            "agencyLevel": 2,
            "agencyLevelSort": "Department of Science\\NASA",
            "appointmentType": "Permanent",
            "workSchedule": "Full-time",
            "payScale": "GS",
            "salaryType": "Per Year",
            "vendor": "USASTAFFING",
            "travelRequirement": "Occasional travel",
            "teleworkEligible": "Y",
            "serviceType": "Competitive",
            "securityClearanceRequired": "Y",
            "securityClearance": "Secret",
            "whoMayApply": "United States Citizens",
            "announcementClosingTypeCode": "C",
            "announcementClosingTypeDescription": "Closing Date",
            "positionOpenDate": "2020-01-01",
            "positionCloseDate": "2020-02-01",
            "positionExpireDate": None,
            "announcementNumber": "NASA-20-001",
            "hiringSubelementName": "Space Operations",
            "positionTitle": "Data Scientist",
            "minimumGrade": "12",
            "maximumGrade": "13",
            "promotionPotential": "13",
            "minimumSalary": 90000.0,
            "maximumSalary": 120000.0,
            "supervisoryStatus": "N",
            "drugTestRequired": "N",
            "relocationExpensesReimbursed": "Y",
            "totalOpenings": "3",
            "disableApplyOnline": "N",
            "positionOpeningStatus": "Accepting Applications",
            "hiringPaths": [{"hiringPath": "The public"}],
            "jobCategories": [{"series": "1550"}],
            "positionLocations": [
                {
                    "positionLocationCity": "Houston",
                    "positionLocationState": "Texas",
                    "positionLocationCountry": "United States",
                }
            ],
        },
        {
            "usajobsControlNumber": 987654321,
            "hiringAgencyCode": "DOE",
            "hiringAgencyName": "Department of Energy",
            "hiringDepartmentCode": "ENG",
            "hiringDepartmentName": "Department of Energy",
            "agencyLevel": 1,
            "agencyLevelSort": "Department of Energy",
            "appointmentType": "Term",
            "workSchedule": "Part-time",
            "payScale": "GS",
            "salaryType": "Per Year",
            "vendor": "OTHER",
            "travelRequirement": "Not required",
            "teleworkEligible": "N",
            "serviceType": None,
            "securityClearanceRequired": "N",
            "securityClearance": "Not Required",
            "whoMayApply": "Agency Employees Only",
            "announcementClosingTypeCode": None,
            "announcementClosingTypeDescription": None,
            "positionOpenDate": "2020-03-01",
            "positionCloseDate": "2020-04-01",
            "positionExpireDate": "2020-04-15",
            "announcementNumber": "DOE-20-ENG",
            "hiringSubelementName": "Energy Research",
            "positionTitle": "Backend Engineer",
            "minimumGrade": "11",
            "maximumGrade": "12",
            "promotionPotential": None,
            "minimumSalary": 80000.0,
            "maximumSalary": 110000.0,
            "supervisoryStatus": "Y",
            "drugTestRequired": "Y",
            "relocationExpensesReimbursed": "N",
            "totalOpenings": "1",
            "disableApplyOnline": "Y",
            "positionOpeningStatus": "Closed",
            "hiringPaths": [{"hiringPath": "Government employees"}],
            "jobCategories": [{"series": "2210"}],
            "positionLocations": [
                {
                    "positionLocationCity": "Washington",
                    "positionLocationState": "District of Columbia",
                    "positionLocationCountry": "United States",
                }
            ],
        },
    ]
