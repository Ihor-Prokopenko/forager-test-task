"""Module providing weather-related functionality."""
from weather_client.exceptions import WeatherAPIClientError, WeatherAPIEndpointError
from weather_client.weather_api_endpoints import WeatherEndpoint, ForecastEndpoint


class WeatherAPIClient(object):
    """
    Represents the weather API client.
    """
    def __init__(self, api_key: str) -> None:
        """Initialize the WeatherAPIClient."""
        self.WEATHER_API_KEY = api_key
        self.weather_endpoint = WeatherEndpoint
        self.forecast_endpoint = ForecastEndpoint

    def get_current_weather(self, city_name: str) -> object:
        """
        Get current weather data for a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            object: The current weather data object for the city.
        """
        weather_endpoint = self.weather_endpoint(self.WEATHER_API_KEY)
        try:
            obj = weather_endpoint.get_current_weather(city_name)
        except WeatherAPIEndpointError as e:
            raise WeatherAPIClientError(str(e))
        return obj

    def get_forecast(self, city_name: str) -> object:
        """
        Get forecast data for a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            object: The forecast data object for the city.
        """
        forecast_endpoint = self.forecast_endpoint(self.WEATHER_API_KEY)
        try:
            obj = forecast_endpoint.get_forecast(city_name)
        except WeatherAPIEndpointError as e:
            raise WeatherAPIClientError(str(e))
        return obj
