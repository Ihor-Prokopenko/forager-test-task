"""Module providing a client for interacting with the Weather API."""

from urllib.parse import urlencode, urljoin

import requests

BASE_URL = 'https://api.weatherapi.com/'
WEATHER_API_PATH = 'v1/current.json'


class WeatherAPIExceptionError(Exception):
    """Exception class for Weather API-related errors."""

    pass


class WeatherAPIClient(object):
    """
    Client for interacting with the Weather API.

    Attributes:
        api_key (str): The API key for accessing the Weather API.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.api_path = WEATHER_API_PATH
        self._validate_api()

    def _validate_api(self):
        """Validate the connection to the Weather API."""
        response = requests.get(self.base_url)
        if not response.status_code == 200:
            raise WeatherAPIExceptionError(f"Failed to connect to Weather API. "
                                      f"Status code: {response.status_code}")

    def _build_url(self, city_name: str = None) -> str:
        """
        Build the full URL for the Weather API request.

        Args:
            city_name (str, optional): The name of the city for which to retrieve weather data.

        Returns:
            str: The full URL for the Weather API request.
        """
        full_url = urljoin(self.base_url, self.api_path)

        params = {"key": self.api_key}
        if city_name:
            params["q"] = city_name

        full_url += "?" + urlencode(params)
        return full_url

    @staticmethod
    def _format_weather_data(data: dict) -> dict:
        """
        Format raw weather data from the API response.

        Args:
            data (dict): Raw weather data from the API response.

        Returns:
            dict: Formatted weather data.
        """
        formatted_data = {
            data.get("location", {}).get("name"): {
                "temperature": data.get("current", {}).get("temp_f"),
                "condition": data.get("current", {}).get("condition", {}).get("text"),
                "last_updated": data.get("current", {}).get("last_updated"),
            }
        }
        return formatted_data

    def get_current_weather(self, city_name: str) -> dict:
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

        return self._format_weather_data(response.json())
