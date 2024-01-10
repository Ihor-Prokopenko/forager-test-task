"""Module providing a service for interacting with the Weather API client."""
from weather_client.exceptions import WeatherAPIClientError, WeatherAPIDataManagerError, WeatherServiceExceptionError
from weather_client.weather_api_client import WeatherAPIClient
from weather_client.weather_data_classes import ForecastResult, WeatherResult
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
        self.weather_data = WeatherResultManager()
        self.forecast_data = ForecastResultManager()

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

    def get_and_save_weather(self, city_name: str) -> WeatherResult | None:
        """
        Get and save the current weather for the specified city.

        Args:
            city_name (str): The name of the city.

        Returns:
            WeatherResult: The current weather for the specified city.
        """
        client: WeatherAPIClient = self._api_client
        try:
            current_weather = client.get_current_weather(city_name=city_name)
        except (WeatherAPIClientError, WeatherAPIDataManagerError) as error:
            raise WeatherServiceExceptionError(str(error))
        return self.weather_data.save(current_weather)

    def get_and_save_forecast(self, city_name: str) -> ForecastResult | None:
        """
        Get and save the forecast for the specified city.

        Args:
            city_name (str): The name of the city.

        Returns:
            ForecastResult: The forecast for the specified city.
        """
        client: WeatherAPIClient = self._api_client
        try:
            forecast = client.get_forecast(city_name=city_name)
        except (WeatherAPIClientError, WeatherAPIDataManagerError) as error:
            raise WeatherServiceExceptionError(str(error))
        return self.forecast_data.save(forecast)
