"""Module providing weather-related functionality."""
from typing import Any, Optional

import requests

from weather_client.exceptions import WeatherAPIRequestError


class BaseWeatherAPIRequest(object):
    """
    Base class for weather API requests.

    Attributes:
        base_url (str): The base URL for the API.
        path (str): The path for the API.
        headers (dict): The headers for the API.
        request_params (dict): The parameters for the API.
        query_params (dict): The query parameters for the API.
    """

    user_agent: str = ''.join([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ',
        '(KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36',
    ])
    headers: dict = {
        'User-Agent': user_agent,
    }
    base_url: str = ''
    path: str = ''
    request_params: dict = {}
    query_params: dict = {}

    def __init__(
            self,
            base_url: str = '',
            path: str = '',
            headers: Optional[dict] = None,
            request_params: Optional[dict] = None,
            query_params: Optional[dict] = None,
    ) -> None:
        """Initialize the BaseWeatherAPIRequest."""
        if base_url:
            self.base_url = base_url
        if not base_url.endswith('/'):
            base_url += '/'
        if path:
            self.path = path
        if headers:
            headers.update(self.headers or {})
            self.headers = headers
        if request_params:
            request_params.update(self.request_params or {})
            self.request_params = request_params
        if query_params:
            query_params.update(self.query_params or {})
            self.query_params = query_params

    def _encode_query_params(self, query_params: Optional[dict] = None) -> str:
        """
        Encode the query parameters.

        Args:
            query_params (dict): The query parameters.

        Returns:
            str: The encoded query parameters.
        """
        if not query_params:
            return ''
        request_params = ['{0}={1}'.format(key, value) for key, value in query_params.items()]
        return '&'.join(request_params)

    def _build_url(self, path: str = '', query_params: Optional[dict] = None) -> str:
        """
        Build the URL for the API request.

        Args:
            path (str): The path for the API.
            query_params (dict): The query parameters for the API.

        Returns:
            str: The URL for the API request.
        """
        if not query_params:
            return self.base_url + path
        self.query_params.update(query_params)
        encoded_query_params = self._encode_query_params(self.query_params)
        return ''.join([self.base_url, path, '?', encoded_query_params])

    def _make_request(self, path: str = '', query_params: Optional[dict] = None) -> requests.Response:
        """
        Make the API request.

        Args:
            path (str): The path for the API.
            query_params (dict): The query parameters for the API.

        Returns:
            requests.Response: The API response.
        """
        url = self._build_url(path, query_params)
        response = requests.get(url, headers=self.headers, params=self.request_params, timeout=5)
        if response.status_code != requests.status_codes.codes.ok:
            message = response.json().get('error', {}).get('message')
            status_code = response.status_code
            raise WeatherAPIRequestError(message, status_code)
        return response
