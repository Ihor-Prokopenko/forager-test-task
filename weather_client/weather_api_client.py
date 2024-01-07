"""Module providing a client for interacting with the Weather API."""
from urllib.parse import urlencode, urljoin

from weather_data_classes import ForecastResult, WeatherResult

from weather_client.mixins import DataParserMixin
from weather_client.weather_api_request_handler import WeatherAPIRequestHandler


class WeatherAPIClient(WeatherAPIRequestHandler, DataParserMixin):
    """
    A class for requesting weather data from the Weather API.

    Attributes:
        _base_url (str): The base URL for the Weather API.
        _current_weather_path (str): The path for the current weather endpoint of the Weather API.
        _forecast_path (str): The path for the forecast endpoint of the Weather API.
        _api_key (str): The API key for accessing the Weather API.
    """

    def request_current_weather(self, city_name: str) -> WeatherResult | None:
        """
        Get the current weather for a specific city from the Weather API.

        Args:
            city_name (str): The name of the city for which to retrieve weather data.

        Returns:
            WeatherResult: Current weather data object for the specified city.
        """
        current_weather_data = self._request_current_weather(city_name)
        if not current_weather_data:
            return None
        return self._weather_data_to_object(current_weather_data)

    def request_forecast(self, city_name: str) -> ForecastResult | None:
        """
        Get the forecast for a specific city from the Weather API.

        Args:
            city_name (str): The name of the city for which to retrieve weather data.

        Returns:
            ForecastResult: Forecast data object for the specified city.
        """
        forecast_data = self._request_forecast(city_name)
        if not forecast_data:
            return None
        return self._forecast_data_to_object(forecast_data)
