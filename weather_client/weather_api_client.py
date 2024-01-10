"""Module providing weather-related functionality."""
from weather_client.weather_api_endpoints import ForecastEndpoint, WeatherEndpoint


class WeatherAPIClient(object):
    """Represents the weather API client."""

    def __init__(self, api_key: str) -> None:
        """Initialize the WeatherAPIClient."""
        self._weather_api_key = api_key
        self.weather = WeatherEndpoint(self._weather_api_key)
        self.forecast = ForecastEndpoint(self._weather_api_key)
