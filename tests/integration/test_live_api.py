"""Live integration tests against the USAJOBS API."""

import datetime as dt
from itertools import islice

from usajobsapi.client import USAJobsClient


def test_search_jobs_live_returns_typed_results(
    integration_client: USAJobsClient,
) -> None:
    """Authenticated search requests should return parsed job results."""

    response = integration_client.search_jobs(
        keyword="engineer",
        results_per_page=2,
    )

    assert response.language == "EN"
    assert response.search_result is not None
    assert response.search_result.result_count is not None
    assert response.search_result.result_count > 0

    jobs = response.jobs()
    assert jobs

    first_job = jobs[0]
    assert first_job.id > 0
    assert first_job.details.position_title
    assert first_job.details.position_uri
    assert first_job.details.organization_name


def test_search_jobs_items_live_iterates_across_pages(
    integration_client: USAJobsClient,
) -> None:
    """The item iterator should stream parsed jobs from paginated search results."""

    jobs = list(
        islice(
            integration_client.search_jobs_items(
                keyword="engineer",
                results_per_page=1,
            ),
            2,
        )
    )

    assert len(jobs) == 2
    assert all(job.id > 0 for job in jobs)
    assert all(job.details.position_title for job in jobs)


def test_historic_joa_live_returns_archived_records() -> None:
    """Historic JOA requests should return parsed archive records."""

    client = USAJobsClient()
    response = client.historic_joa(
        start_position_open_date=dt.date(2020, 1, 1),
        end_position_open_date=dt.date(2020, 1, 31),
    )

    assert response.data

    first_item = response.data[0]
    assert first_item.usajobs_control_number > 0
    assert first_item.position_title
    assert first_item.position_open_date is not None
    assert first_item.position_open_date >= dt.date(2020, 1, 1)
    assert first_item.position_open_date <= dt.date(2020, 1, 31)
