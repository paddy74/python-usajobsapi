"""Integration testing fixtures."""

import os

import pytest

from usajobsapi.client import USAJobsClient


@pytest.fixture(scope="session")
def integration_auth_user() -> str:
    """Return the configured User-Agent email for live API integration tests."""

    value = os.environ.get("USAJOBS_USER_AGENT")
    if not value:
        pytest.skip("Set USAJOBS_USER_AGENT to run integration tests.")
    return value


@pytest.fixture(scope="session")
def integration_auth_key() -> str:
    """Return the configured API key for live API integration tests."""

    value = os.environ.get("USAJOBS_API_KEY")
    if not value:
        pytest.skip("Set USAJOBS_API_KEY to run integration tests.")
    return value


@pytest.fixture(scope="session")
def integration_client(
    integration_auth_user: str, integration_auth_key: str
) -> USAJobsClient:
    """Create a live API client for integration tests."""

    return USAJobsClient(
        auth_user=integration_auth_user,
        auth_key=integration_auth_key,
        timeout=60,
    )
