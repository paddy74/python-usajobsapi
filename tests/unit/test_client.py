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
