"""Module providing a client for interacting with the Weather API."""
from urllib.parse import urlencode, urljoin

import requests

BASE_URL = 'https://api.weatherapi.com/'
WEATHER_API_PATH = 'v1/current.json'


class WeatherAPIExceptionError(Exception):
    """Exception class for Weather API-related errors."""

    pass


class WeatherResult(object):
    """
    Represents the weather result for a city.

    Attributes:
        city_name (str): The name of the city.
        temperature (float): The temperature in Celsius.
        condition (str): The weather condition description.
        last_updated (str): The timestamp of the last update.
    """

    def __init__(self, city_name: str, temperature: int | float, condition: str, last_updated: str) -> None:
        """
        Initialize the WeatherResult.
        Args:
            city_name:
            temperature:
            condition:
            last_updated:
        """

        self.city_name = city_name
        self.temperature = temperature
        self.condition = condition
        self.last_updated = last_updated

    def __str__(self) -> str:
        """Returns a string representation of the WeatherResult."""
        return (f"City: {self.city_name}, Temp: {self.temperature}, "
                f"Condition: {self.condition}, Last Updated: {self.last_updated}")


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
            api_key:
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
            raise WeatherAPIExceptionError("Invalid API key type. Expected: str")
        self._api_key = api_key

    def _build_url(self, city_name) -> str:
        """
        Build the full URL for the Weather API request.

        Args:
            city_name (str): The name of the city for which to retrieve weather data.

        Returns:
            str: The full URL for the Weather API request.
        """

        full_url = urljoin(self._base_url, self._api_path)

        params = {
            'key': self._api_key,
            'q': city_name,
        }
        full_url += '?' + urlencode(params)
        return full_url

    def _validate_api(self) -> None:
        """Validate the connection to the Weather API."""

        response = requests.get(self._base_url)
        if not response.status_code == 200:
            raise WeatherAPIExceptionError(f"Failed to connect to Weather API. "
                                           f"Status code: {response.status_code}")

    @staticmethod
    def _weather_data_to_object(data: dict) -> WeatherResult:
        """
        Args:
            data: dict: Weather data.

        Returns:
            WeatherResult:
        """

        formatted_data = {
                'city_name': data.get('location', {}).get('name'),
                'temperature': data.get('current', {}).get('temp_c'),
                'condition': data.get('current', {}).get('condition', {}).get('text'),
                'last_updated': data.get('current', {}).get('last_updated'),
        }
        return WeatherResult(**formatted_data)

    def get_current_weather(self, city_name: str) -> WeatherResult:
        """
        Get the current weather for a specific city from the Weather API.

        Args:
            city_name (str, optional): The name of the city for which to retrieve weather data.

        Returns:
            dict: Current weather data for the specified city.
        """

        url = self._build_url(city_name)
        response = requests.get(url)
        if not response.status_code == 200:
            raise WeatherAPIExceptionError(f"{response.json().get('error', {}).get('message')} "
                                           f"Status code: {response.status_code}")
        return self._weather_data_to_object(response.json())
