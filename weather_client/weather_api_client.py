"""Module providing weather-related functionality."""
from weather_client.exceptions import WeatherAPIClientError, WeatherAPIEndpointError
from weather_client.weather_api_endpoints import ForecastEndpoint, WeatherEndpoint
from weather_client.weather_data_classes import ForecastResult, WeatherResult


class WeatherAPIClient(object):
    """Represents the weather API client."""

    def __init__(self, api_key: str) -> None:
        """Initialize the WeatherAPIClient."""
        self._weather_api_key = api_key
        self.weather_endpoint = WeatherEndpoint
        self.forecast_endpoint = ForecastEndpoint

    def get_current_weather(self, city_name: str) -> WeatherResult:
        """
        Get current weather data for a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            WeatherResult: The current weather data object for the city.
        """
        weather_endpoint = self.weather_endpoint(self._weather_api_key)
        try:
            weather_obj = weather_endpoint.get_current_weather(city_name)
        except WeatherAPIEndpointError as error:
            raise WeatherAPIClientError(str(error))
        return weather_obj

    def get_forecast(self, city_name: str) -> ForecastResult:
        """
        Get forecast data for a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            ForecastResult: The forecast data object for the city.
        """
        forecast_endpoint = self.forecast_endpoint(self._weather_api_key)
        try:
            forecast_obj = forecast_endpoint.get_forecast(city_name)
        except WeatherAPIEndpointError as error:
            raise WeatherAPIClientError(str(error))
        return forecast_obj
