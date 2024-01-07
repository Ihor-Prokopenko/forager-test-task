"""Module providing a service for interacting with the Weather API client."""
from weather_data_classes import ForecastResult, WeatherResult
from weather_data_managers import ForecastResultManager, WeatherResultManager

from weather_client.exceptions import WeatherServiceExceptionError
from weather_client.weather_api_client import WeatherAPIClient


class WeatherService(WeatherResultManager, ForecastResultManager):
    """
    Handles weather-related operations and results.

    Attributes:
        _api_client (WeatherAPIClient): An instance of the WeatherAPIClient class.

    Methods:
        request_current_weather(self, city_name: str | list[str])
        request_forecast(self, city_name: str | list[str])
        save_weather(self, result_obj: WeatherResult | list[WeatherResult])
        save_forecasts(self, result_obj: ForecastResult | list[ForecastResult])
        clear_weather(self, city_name: str | list[str])
        clear_forecast(self, city_name: str | list[str])
    """

    def __init__(self, api_client: WeatherAPIClient) -> None:
        """
        Initialize the WeatherService.

        Args:
            api_client: An instance of the WeatherAPIClient class.
        """
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

    def request_current_weather(self, city_name: str | list[str]) -> WeatherResult | list[WeatherResult]:
        """
        Get and save the current weather for one or multiple cities.

        Args:
            city_name (str or list[str]): The name of the city or a list of city names.

        Returns:
            WeatherResult or list[WeatherResult]: The current weather for the specified city or cities.
        """
        client: WeatherAPIClient = self._api_client
        if isinstance(city_name, list):
            return self.save_weather([client.request_current_weather(city_name=city) for city in city_name])
        elif isinstance(city_name, str):
            return self.save_weather(client.request_current_weather(city_name=city_name))

    def request_forecast(self, city_name: str | list[str]) -> ForecastResult | list[ForecastResult]:
        """
        Get and save the forecast for one or multiple cities.

        Args:
            city_name (str or list[str]): The name of the city or a list of city names.

        Returns:
            ForecastResult or list[ForecastResult]: The forecast for the specified city or cities.
        """
        client: WeatherAPIClient = self._api_client
        if isinstance(city_name, list):
            return self.save_forecasts([client.request_forecast(city_name=city) for city in city_name])
        elif isinstance(city_name, str):
            return self.save_forecasts(client.request_forecast(city_name=city_name))
