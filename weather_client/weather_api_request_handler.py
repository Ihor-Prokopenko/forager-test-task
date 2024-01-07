"""Module providing weather-related functionality."""
from urllib.parse import urlencode, urljoin

import requests

from weather_client.exceptions import WeatherAPIExceptionError
from weather_client.settings import BASE_URL, CURRENT_WEATHER_PATH, FORECAST_PATH


class WeatherAPIRequestHandler(object):
    """
    Handles requests to the Weather API.

    Attributes:
        _api_key (str): The API key for accessing the Weather API.
        _base_url (str): The base URL for the Weather API.
        _current_weather_path (str): The path for the current weather endpoint of the Weather API.
        _forecast_path (str): The path for the forecast endpoint of the Weather API.

    Methods:
        _validate_api(self)
        _build_url(self, path, city_name: str)
        _request_current_weather(self, city_name)
        _request_forecast(self, city_name)
    """

    def __init__(self, api_key: str) -> None:
        """
        Initialize the WeatherAPIClient.

        Args:
            api_key: The API key for accessing the Weather API.
        """
        self._api_key = api_key
        self._base_url = BASE_URL
        self._current_weather_path = CURRENT_WEATHER_PATH
        self._forecast_path = FORECAST_PATH
        self._validate_api()

    @property
    def api_key(self) -> str:
        """Getter for the API key."""
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str) -> None:
        """Setter for the API key."""
        if not isinstance(api_key, str):
            raise WeatherAPIExceptionError('Invalid API key type. Expected: str')
        self._api_key = api_key

    def _validate_api(self) -> None:
        """Validate the connection to the Weather API."""
        response = requests.get(self._base_url, timeout=5)
        if response.status_code != requests.codes.ok:
            error_message = 'Failed to connect to Weather API. Status code: {0}'.format(response.status_code)
            raise WeatherAPIExceptionError(error_message)

    def _build_url(self, path: str, city_name: str) -> str:
        """
        Build the full URL for the Weather API request.

        Args:
            path (str): The path for the endpoint of the Weather API.
            city_name (str): The name of the city for which to retrieve weather data.

        Returns:
            str: The full URL for the Weather API request.
        """
        url = urljoin(self._base_url, path)

        query_params = {
            'key': self._api_key,
            'q': city_name,
        }
        params_string = urlencode(query_params)
        return '{0}?{1}'.format(url, params_string)

    def _request_current_weather(self, city_name: str) -> dict:
        """
        Request current weather data from the Weather API.

        Args:
            city_name (str): The name of the city for which to retrieve weather data.

        Returns:
            dict: The response from the Weather API.
        """
        url = self._build_url(self._current_weather_path, city_name)
        response = requests.get(url, timeout=5)
        if response.status_code != requests.codes.ok:
            error_message = 'Failed to retrieve weather data. Status code: {0}'.format(response.status_code)
            raise WeatherAPIExceptionError(error_message)
        return response.json()

    def _request_forecast(self, city_name: str) -> dict:
        """
        Request forecast data from the Weather API.

        Args:
            city_name (str): The name of the city for which to retrieve weather data.

        Returns:
            dict: The response from the Weather API.
        """
        url = self._build_url(self._forecast_path, city_name)
        response = requests.get(url, timeout=5)
        if response.status_code != requests.codes.ok:
            error_message = 'Failed to retrieve weather data. Status code: {0}'.format(response.status_code)
            raise WeatherAPIExceptionError(error_message)
        return response.json()
