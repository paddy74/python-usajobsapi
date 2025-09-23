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
            "positionTitle": "Data Scientist",
            "hiringAgencyCode": "NASA",
            "hiringDepartmentCode": "NAT",
            "positionOpenDate": "2020-01-01",
            "positionCloseDate": "2020-02-01",
            "minimumSalary": 90000.0,
            "maximumSalary": 120000.0,
        },
        {
            "usajobsControlNumber": 987654321,
            "positionTitle": "Backend Engineer",
            "hiringAgencyCode": "DOE",
            "hiringDepartmentCode": "ENG",
            "positionOpenDate": "2020-03-01",
            "positionCloseDate": "2020-04-01",
            "minimumSalary": 80000.0,
            "maximumSalary": 110000.0,
        },
    ]
