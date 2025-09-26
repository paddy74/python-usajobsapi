"""Wrapper for the USAJOBS REST API."""

from collections.abc import Iterator
from typing import Dict, Optional
from urllib.parse import urlparse

import requests

from usajobsapi.endpoints import (
    AnnouncementTextEndpoint,
    HistoricJoaEndpoint,
    SearchEndpoint,
)


class USAJobsApiClient:
    """Represents a client connection to the USAJOBS REST API."""

    def __init__(
        self,
        url: Optional[str] = "https://data.usajobs.gov",
        ssl_verify: bool = True,
        timeout: Optional[float] = 60,
        auth_user: Optional[str] = None,
        auth_key: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        """
        :param url: The URL of the USAJOBS REST API server, defaults to "https://data.usajobs.gov"
        :type url: str | None, optional
        :param ssl_verify: Whether SSL certificates should be validated, defaults to True
        :type ssl_verify: bool, optional
        :param timeout: Timeout to use for requests to the USA JOBS REST API, defaults to 60s
        :type timeout: float | None, optional
        :param auth_user: Email address associated with the API key, defaults to None
        :type auth_user: str | None, optional
        :param auth_key: API key used for the Job Search API, defaults to None
        :type auth_key: str | None, optional
        :param session: _description_, defaults to None
        :type session: requests.Session | None, optional
        """
        self._url = url

        # Timeout to use for requests to the server
        self.timeout = timeout

        # Whether SSL certificates should be validated
        self.ssl_verify = ssl_verify

        # Headers used for the Job Search API
        self.headers = {
            "Host": urlparse(self._url).hostname,
            "User-Agent": auth_user,
            "Authorization-Key": auth_key,
        }

        self._session = session or requests.Session()

    def _build_url(self, path: str) -> str:
        """Returns the full URL from the given path.

        If the path is already a URL, return it unchanged. If it is a path, append it to the stored base URL.

        :param path: A URL path.
        :type path: str
        :return: The full URL with the given path.
        :rtype: str
        """
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self._url}{path}"

    def _request(
        self, method: str, path: str, params: Dict[str, str], add_auth: bool = False
    ) -> requests.Response:
        """Helper method for sending HTTP requests.

        :param method: HTTP method
        :type method: str
        :param path: Request URL
        :type path: str
        :param params: Request query parameters
        :type params: Dict[str, str]
        :param add_auth: If true, includes the stored authentication headers with the request, defaults to False
        :type add_auth: bool, optional
        :return: Request response
        :rtype: requests.Response
        """
        url = self._build_url(path)
        headers = self.headers if add_auth else {}

        # Send the request
        resp = self._session.request(
            method, url, params=params, headers=headers, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp

    def announcement_text(self, **kwargs) -> AnnouncementTextEndpoint.Response:
        """Query the Announcement Text API.

        :return: _description_
        :rtype: AnnouncementTextEndpoint.Response
        """
        params = AnnouncementTextEndpoint.Params(**kwargs)
        resp = self._request(
            AnnouncementTextEndpoint.model_fields["method"].default,
            AnnouncementTextEndpoint.model_fields["path"].default,
            params.to_params(),
        )
        return AnnouncementTextEndpoint.Response.model_validate(resp.json())

    def job_search(self, **kwargs) -> SearchEndpoint.Response:
        """Query the Job Search API.

        :return: _description_
        :rtype: SearchEndpoint.Response
        """
        params = SearchEndpoint.Params(**kwargs)
        resp = self._request(
            SearchEndpoint.model_fields["method"].default,
            SearchEndpoint.model_fields["path"].default,
            params.to_params(),
            add_auth=True,
        )
        return SearchEndpoint.Response.model_validate(resp.json())

    def historic_joa(self, **kwargs) -> HistoricJoaEndpoint.Response:
        """Query the Historic JOAs API.

        :return: _description_
        :rtype: HistoricJoaEndpoint.Response
        """
        params = HistoricJoaEndpoint.Params(**kwargs)
        resp = self._request(
            HistoricJoaEndpoint.model_fields["METHOD"].default,
            HistoricJoaEndpoint.model_fields["PATH"].default,
            params.to_params(),
        )
        return HistoricJoaEndpoint.Response.model_validate(resp.json())

    def historic_joa_pages(self, **kwargs) -> Iterator[HistoricJoaEndpoint.Response]:
        """Yield Historic JOA pages, following continuation tokens.

        This can handle fresh requests or continue from a response page with a continuation token.

        :raises RuntimeError: On a duplicate continuation token.
        :yield: The response object for the given continuation token.
        :rtype: Iterator[HistoricJoaEndpoint.Response]
        """

        # Get the token by object name or alias name
        token = kwargs.pop("continuationToken", kwargs.pop("continuation_token", None))

        seen_tokens: set[str] = set()
        if token:
            seen_tokens.add(token)

        while True:
            call_kwargs = kwargs
            if token:
                call_kwargs["continuation_token"] = token

            resp = self.historic_joa(**call_kwargs)

            next_token = resp.next_token()
            # Handle duplicate tokens
            if next_token and next_token in seen_tokens:
                raise RuntimeError(
                    f"Historic JOA pagination returned duplicate continuation token '{next_token}'"
                )

            yield resp

            # If more pages
            if not next_token:
                break

            seen_tokens.add(next_token)
            token = next_token

    def historic_joa_items(self, **kwargs) -> Iterator[HistoricJoaEndpoint.Item]:
        """Yield Historic JOA items, following continuation tokens.

        This can handle fresh requests or continue from a response page with a continuation token.

        :raises RuntimeError: On a duplicate continuation token.
        :yield: The response item.
        :rtype: Iterator[HistoricJoaEndpoint.Item]
        """
        token = kwargs.pop("continuationToken", kwargs.pop("continuation_token", None))

        seen_tokens: set[str] = set()
        if token:
            seen_tokens.add(token)

        while True:
            call_kwargs = kwargs
            if token:
                call_kwargs["continuation_token"] = token

            resp = self.historic_joa(**call_kwargs)

            for item in resp.data:
                yield item

            next_token = resp.next_token()
            # Handle duplicate tokens
            if next_token and next_token in seen_tokens:
                raise RuntimeError(
                    f"Historic JOA pagination returned duplicate continuation token '{next_token}'"
                )

            if not next_token:
                break

            seen_tokens.add(next_token)
            token = next_token
