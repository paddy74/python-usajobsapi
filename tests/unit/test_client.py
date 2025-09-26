"""Unit tests for USAJobsApiClient."""

from copy import deepcopy

import pytest

from usajobsapi.client import USAJobsApiClient
from usajobsapi.endpoints.historicjoa import HistoricJoaEndpoint

# test historic_joa_pages
# ---


def test_historic_joa_pages_yields_pages(
    monkeypatch, historicjoa_response_payload
) -> None:
    """Ensure historic_joa_pages yields pages while forwarding continuation tokens."""

    first_payload = deepcopy(historicjoa_response_payload)
    second_payload = deepcopy(historicjoa_response_payload)
    second_payload["paging"]["metadata"]["continuationToken"] = None
    second_payload["data"] = []

    responses = [
        HistoricJoaEndpoint.Response.model_validate(first_payload),
        HistoricJoaEndpoint.Response.model_validate(second_payload),
    ]
    captured_kwargs = []

    def fake_historic_joa(self, **call_kwargs):
        captured_kwargs.append(call_kwargs)
        return responses.pop(0)

    monkeypatch.setattr(USAJobsApiClient, "historic_joa", fake_historic_joa)

    client = USAJobsApiClient()

    pages = list(
        client.historic_joa_pages(
            hiring_agency_codes="NASA", continuation_token="INITIALTOKEN"
        )
    )

    assert len(pages) == 2
    assert pages[0].next_token() == "NEXTTOKEN"
    assert pages[1].next_token() is None
    assert captured_kwargs == [
        {"hiring_agency_codes": "NASA", "continuation_token": "INITIALTOKEN"},
        {"hiring_agency_codes": "NASA", "continuation_token": "NEXTTOKEN"},
    ]


def test_historic_joa_pages_duplicate_token(
    monkeypatch, historicjoa_response_payload
) -> None:
    """Duplicate continuation tokens should raise to avoid infinite loops."""

    first_response = HistoricJoaEndpoint.Response.model_validate(
        historicjoa_response_payload
    )
    duplicate_payload = deepcopy(historicjoa_response_payload)
    duplicate_payload["paging"]["metadata"]["continuationToken"] = (
        first_response.next_token()
    )
    responses = [
        first_response,
        HistoricJoaEndpoint.Response.model_validate(duplicate_payload),
    ]

    def fake_historic_joa(self, **_):
        return responses.pop(0)

    monkeypatch.setattr(USAJobsApiClient, "historic_joa", fake_historic_joa)

    client = USAJobsApiClient()
    iterator = client.historic_joa_pages()

    assert next(iterator)
    with pytest.raises(RuntimeError, match="duplicate continuation token"):
        next(iterator)


# test historic_joa_items
# ---


def test_historic_joa_items_yields_items_across_pages(
    monkeypatch: pytest.MonkeyPatch, historicjoa_response_payload
) -> None:
    """Ensure historic_joa_items yields items and follows continuation tokens."""

    client = USAJobsApiClient()

    first_page = deepcopy(historicjoa_response_payload)
    first_page["paging"]["metadata"]["continuationToken"] = "TOKEN2"
    first_page["data"] = first_page["data"][:2]

    second_page = {
        "paging": {
            "metadata": {"totalCount": 3, "pageSize": 1, "continuationToken": None},
            "next": None,
        },
        "data": [
            {
                "usajobsControlNumber": 111222333,
                "hiringAgencyCode": "GSA",
                "hiringAgencyName": "General Services Administration",
                "hiringDepartmentCode": "GSA",
                "hiringDepartmentName": "General Services Administration",
                "agencyLevel": 1,
                "agencyLevelSort": "GSA",
                "appointmentType": "Permanent",
                "workSchedule": "Full-time",
                "payScale": "GS",
                "salaryType": "Per Year",
                "vendor": "USASTAFFING",
                "travelRequirement": "Not required",
                "teleworkEligible": "Y",
                "serviceType": "Competitive",
                "securityClearanceRequired": "N",
                "securityClearance": "Not Required",
                "whoMayApply": "All",
                "announcementClosingTypeCode": "C",
                "announcementClosingTypeDescription": "Closing Date",
                "positionOpenDate": "2020-05-01",
                "positionCloseDate": "2020-05-15",
                "positionExpireDate": None,
                "announcementNumber": "GSA-20-001",
                "hiringSubelementName": "Administration",
                "positionTitle": "Systems Analyst",
                "minimumGrade": "11",
                "maximumGrade": "12",
                "promotionPotential": "13",
                "minimumSalary": 85000.0,
                "maximumSalary": 95000.0,
                "supervisoryStatus": "N",
                "drugTestRequired": "N",
                "relocationExpensesReimbursed": "N",
                "totalOpenings": "2",
                "disableApplyOnline": "N",
                "positionOpeningStatus": "Accepting Applications",
                "hiringPaths": [{"hiringPath": "The public"}],
                "jobCategories": [{"series": "2210"}],
                "positionLocations": [
                    {
                        "positionLocationCity": "Washington",
                        "positionLocationState": "District of Columbia",
                        "positionLocationCountry": "United States",
                    }
                ],
            }
        ],
    }

    responses = [first_page, second_page]
    calls = []

    def fake_historic(**call_kwargs):
        calls.append(call_kwargs)
        return HistoricJoaEndpoint.Response.model_validate(responses.pop(0))

    monkeypatch.setattr(client, "historic_joa", fake_historic)

    items = list(client.historic_joa_items(hiring_agency_codes="NASA"))

    assert [item.usajobs_control_number for item in items] == [
        123456789,
        987654321,
        111222333,
    ]
    assert len(calls) == 2
    assert "continuation_token" not in calls[0]
    assert calls[1]["continuation_token"] == "TOKEN2"


def test_historic_joa_items_respects_initial_token(
    monkeypatch: pytest.MonkeyPatch, historicjoa_response_payload
) -> None:
    """Ensure historic_joa_items uses the supplied initial continuation token."""

    client = USAJobsApiClient()

    payload = deepcopy(historicjoa_response_payload)
    payload["paging"]["metadata"]["continuationToken"] = None

    calls = []

    def fake_historic(**call_kwargs):
        calls.append(call_kwargs)
        return HistoricJoaEndpoint.Response.model_validate(payload)

    monkeypatch.setattr(client, "historic_joa", fake_historic)

    items = list(client.historic_joa_items(continuation_token="SEED"))

    assert len(items) == len(payload["data"])
    assert calls[0]["continuation_token"] == "SEED"
