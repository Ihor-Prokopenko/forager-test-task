"""Module providing a service for interacting with the Weather API client."""
from weather_client.exceptions import WeatherServiceExceptionError
from weather_client.weather_api_client import WeatherAPIClient
from weather_client.weather_data_managers import ForecastResultManager, WeatherResultManager


class WeatherService(object):
    """Handles weather-related operations and results."""

    def __init__(self, api_client: WeatherAPIClient) -> None:
        """
        Initialize the WeatherService.

        Args:
            api_client: An instance of the WeatherAPIClient class.
        """
        self._api_client = api_client
        self.weather_data = WeatherResultManager(self._api_client)
        self.forecast_data = ForecastResultManager(self._api_client)

    @property
    def api_client(self) -> WeatherAPIClient:
        """Getter for the API client."""
        return self._api_client

    @api_client.setter
    def api_client(self, api_client: WeatherAPIClient) -> None:
        """Setter for the API client."""
        if not isinstance(api_client, WeatherAPIClient):
            raise WeatherServiceExceptionError('Invalid API client type. Expected: WeatherAPIClient')
        self._api_client = api_client
