"""Module providing a service for interacting with the Weather API client."""
from weather_client.weather_client import WeatherAPIClient, WeatherResult
from weather_client.weather_data_managers import WeatherResultManager
from weather_client.exceptions import WeatherServiceExceptionError
from weather_client.weather_data_classes import WeatherResult


class WeatherService(WeatherResultManager):
    """
    Handles weather-related operations and results.

    Attributes:
        _api_client (WeatherAPIClient): An instance of the WeatherAPIClient class.
    """

    def __init__(self, api_client: WeatherAPIClient) -> None:
        """
        Initialize the WeatherService.

        Args:
            api_client: An instance of the WeatherAPIClient class.
        """
        super().__init__()
        self._api_client = api_client

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

    def get_current_weather(self, city_name: str | list[str]) -> WeatherResult | list[WeatherResult]:
        """
        Get and save the current weather for one or multiple cities.

        Args:
            city_name (str or list[str]): The name of the city or a list of city names.

        Returns:
            WeatherResult or list[WeatherResult]: The current weather for the specified city or cities.
        """
        client: WeatherAPIClient = self._api_client
        if isinstance(city_name, list):
            return self.save_results([client.get_current_weather(city_name=city) for city in city_name])
        elif isinstance(city_name, str):
            return self.save_results(client.get_current_weather(city_name=city_name))
