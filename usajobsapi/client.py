"""Wrapper for the USAJOBS REST API."""

from urllib.parse import urlparse


class USAJobsApiClient:
    """Represents a client connection to the USAJOBS REST API."""

    def __init__(
        self,
        url: str | None = "https://data.usajobs.gov",
        ssl_verify: bool = True,
        timeout: float | None = None,
        auth_user: str | None = None,
        auth_key: str | None = None,
    ) -> None:
        """
        :param url: The URL of the USAJOBS REST API server, defaults to "https://data.usajobs.gov"
        :type url: str | None, optional
        :param ssl_verify: Whether SSL certificates should be validated, defaults to True
        :type ssl_verify: bool, optional
        :param timeout: Timeout to use for requests to the USA JOBS REST API, defaults to None
        :type timeout: float | None, optional
        :param auth_user: Email address associated with the API key, defaults to None
        :type auth_user: str | None, optional
        :param auth_key: API key used for the Job Search API, defaults to None
        :type auth_key: str | None, optional
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
