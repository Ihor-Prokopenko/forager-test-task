"""Module providing a client for interacting with the Weather API."""
from urllib.parse import urlencode, urljoin
from weather_client.exceptions import WeatherAPIExceptionError
from weather_client.weather_data_classes import WeatherResult

import requests

BASE_URL = 'https://api.weatherapi.com/'
WEATHER_API_PATH = 'v1/current.json'


class WeatherAPIClient(object):
    """
    Client for interacting with the Weather API.

    Attributes:
        _api_key (str): The API key for accessing the Weather API.
        _base_url (str): The base URL for the Weather API.
        _api_path (str): The path for the current weather endpoint of the Weather API.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initialize the WeatherAPIClient.

        Args:
            api_key: The API key for accessing the Weather API.
        """
        self._api_key = api_key
        self._base_url = BASE_URL
        self._api_path = WEATHER_API_PATH
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

    def _build_url(self, city_name: str) -> str:
        """
        Build the full URL for the Weather API request.

        Args:
            city_name (str): The name of the city for which to retrieve weather data.

        Returns:
            str: The full URL for the Weather API request.
        """
        url = urljoin(self._base_url, self._api_path)

        query_params = {
            'key': self._api_key,
            'q': city_name,
        }
        params_string = urlencode(query_params)
        return '{0}?{1}'.format(url, params_string)

    def _weather_data_to_object(self, weather_data: dict) -> WeatherResult:
        """
        Convert weather data to a WeatherResult object.

        Args:
            weather_data: dict: Weather data.

        Returns:
            WeatherResult: Weather result object.
        """
        formatted_data = {
            'city_name': weather_data.get('location', {}).get('name'),
            'temperature': weather_data.get('current', {}).get('temp_c'),
            'condition': weather_data.get('current', {}).get('condition', {}).get('text'),
            'last_updated': weather_data.get('current', {}).get('last_updated'),
        }
        return WeatherResult(**formatted_data)

    def get_current_weather(self, city_name: str) -> WeatherResult:
        """
        Get the current weather for a specific city from the Weather API.

        Args:
            city_name (str): The name of the city for which to retrieve weather data.

        Returns:
            WeatherResult: Current weather data object for the specified city.
        """
        url = self._build_url(city_name)
        response = requests.get(url, timeout=5)
        error_message = response.json().get('error', {}).get('message')
        status_code = response.status_code
        if response.status_code != requests.codes.ok:
            error_message = '{0}Status code: {1}'.format(error_message, status_code)
            raise WeatherAPIExceptionError(error_message)
        return self._weather_data_to_object(response.json())
