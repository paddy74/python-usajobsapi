"""Unit tests for USAJobsClient."""

from copy import deepcopy

import pytest

from usajobsapi.client import USAJobsClient
from usajobsapi.endpoints.historicjoa import HistoricJoaEndpoint
from usajobsapi.endpoints.search import SearchEndpoint

# test search_jobs_pages
# ---


def _build_search_payload(items, count, total=None):
    """Build a serialized SearchResult payload for mocked responses."""

    payload = {
        "SearchResult": {
            "SearchResultCount": count,
            "SearchResultItems": items,
        }
    }
    if total is not None:
        payload["SearchResult"]["SearchResultCountAll"] = total
    return payload


def test_search_jobs_pages_yields_pages(monkeypatch, search_result_item) -> None:
    """Ensure search_jobs_pages iterates pages based on total counts."""

    first_item = deepcopy(search_result_item)
    first_item["MatchedObjectDescriptor"]["MatchedObjectId"] = "1"
    second_item = deepcopy(search_result_item)
    second_item["MatchedObjectDescriptor"]["MatchedObjectId"] = "2"
    third_item = deepcopy(search_result_item)
    third_item["MatchedObjectDescriptor"]["MatchedObjectId"] = "3"
    fourth_item = deepcopy(search_result_item)
    fourth_item["MatchedObjectDescriptor"]["MatchedObjectId"] = "4"
    fifth_item = deepcopy(search_result_item)
    fifth_item["MatchedObjectDescriptor"]["MatchedObjectId"] = "5"

    responses = [
        SearchEndpoint.Response.model_validate(
            _build_search_payload([first_item, second_item], 2, total=5)
        ),
        SearchEndpoint.Response.model_validate(
            _build_search_payload([third_item, fourth_item], 2, total=5)
        ),
        SearchEndpoint.Response.model_validate(
            _build_search_payload([fifth_item], 1, total=5)
        ),
    ]

    captured_kwargs = []

    def fake_search(self, **call_kwargs):
        captured_kwargs.append(call_kwargs)
        return responses.pop(0)

    monkeypatch.setattr(USAJobsClient, "search_jobs", fake_search)

    client = USAJobsClient()
    pages = list(client.search_jobs_pages(keyword="engineer", results_per_page=2))

    assert len(pages) == 3
    assert [call["page"] for call in captured_kwargs] == [1, 2, 3]
    assert all(call["results_per_page"] == 2 for call in captured_kwargs)


def test_search_jobs_pages_handles_missing_total(
    monkeypatch, search_result_item
) -> None:
    """Continue until a short page is returned when total counts are absent."""

    first_page = SearchEndpoint.Response.model_validate(
        _build_search_payload(
            [deepcopy(search_result_item), deepcopy(search_result_item)],
            2,
        )
    )
    second_item = deepcopy(search_result_item)
    second_item["MatchedObjectDescriptor"]["MatchedObjectId"] = "3"
    second_page = SearchEndpoint.Response.model_validate(
        _build_search_payload([second_item], 1)
    )

    responses = [first_page, second_page]
    captured_kwargs = []

    def fake_search(self, **call_kwargs):
        captured_kwargs.append(call_kwargs)
        return responses.pop(0)

    monkeypatch.setattr(USAJobsClient, "search_jobs", fake_search)

    client = USAJobsClient()
    pages = list(client.search_jobs_pages(keyword="space"))

    assert len(pages) == 2
    assert [call["page"] for call in captured_kwargs] == [1, 2]
    assert "results_per_page" not in captured_kwargs[0]
    assert captured_kwargs[1]["results_per_page"] == 2


def test_search_jobs_pages_breaks_on_empty_results(monkeypatch) -> None:
    """Stop pagination when a page returns no results."""

    empty_page = SearchEndpoint.Response.model_validate(
        {"SearchResult": {"SearchResultCount": 0, "SearchResultItems": []}}
    )

    def fake_search(self, **_):
        return empty_page

    monkeypatch.setattr(USAJobsClient, "search_jobs", fake_search)

    client = USAJobsClient()
    pages = list(client.search_jobs_pages(keyword="empty"))

    assert len(pages) == 1


# test search_jobs_items
# ---


def _search_response_payload(
    items: list[dict],
    count: int,
    total: int,
    page: int,
    results_per_page: int,
) -> dict:
    return {
        "LanguageCode": "EN",
        "SearchParameters": {
            "page": page,
            "results_per_page": results_per_page,
        },
        "SearchResult": {
            "SearchResultCount": count,
            "SearchResultCountAll": total,
            "SearchResultItems": items,
        },
    }


def test_search_jobs_items_yields_jobs(monkeypatch, job_summary_payload) -> None:
    """Ensure search_jobs_items yields summaries across pages."""

    client = USAJobsClient()

    first_payload = deepcopy(job_summary_payload)
    first_payload["MatchedObjectId"] = "1"
    second_payload = deepcopy(job_summary_payload)
    second_payload["MatchedObjectId"] = "2"
    third_payload = deepcopy(job_summary_payload)
    third_payload["MatchedObjectId"] = "3"

    responses = [
        _search_response_payload(
            [
                {"MatchedObjectDescriptor": first_payload},
                {"MatchedObjectDescriptor": second_payload},
            ],
            2,
            3,
            1,
            2,
        ),
        _search_response_payload(
            [{"MatchedObjectDescriptor": third_payload}],
            1,
            3,
            2,
            2,
        ),
    ]

    def fake_search_jobs(self, **_):
        return SearchEndpoint.Response.model_validate(responses.pop(0))

    monkeypatch.setattr(USAJobsClient, "search_jobs", fake_search_jobs)

    summaries = list(client.search_jobs_items(results_per_page=2))

    assert [summary.id for summary in summaries] == ["1", "2", "3"]


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

    monkeypatch.setattr(USAJobsClient, "historic_joa", fake_historic_joa)

    client = USAJobsClient()

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

    monkeypatch.setattr(USAJobsClient, "historic_joa", fake_historic_joa)

    client = USAJobsClient()
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

    client = USAJobsClient()

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

    client = USAJobsClient()

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
