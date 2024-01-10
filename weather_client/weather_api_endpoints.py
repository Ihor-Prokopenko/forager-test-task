"""Module providing weather-related functionality."""
from typing import Any, Optional, Type

from weather_client.data_parsers import BaseDataParser, ForecastDataParser, WeatherDataParser
from weather_client.exceptions import DataParserError, WeatherAPIEndpointError, WeatherAPIRequestError
from weather_client.settings import BASE_URL, CURRENT_WEATHER_PATH, FORECAST_PATH
from weather_client.weather_api_requests import BaseWeatherAPIRequest


class BaseWeatherAPIEndpoint(BaseWeatherAPIRequest):
    """
    Base class for weather API endpoints.

    Attributes:
        base_url (str): The base URL for the API.
        path (str): The path for the API.
    """

    base_url: str = BASE_URL
    data_parser: type = BaseDataParser

    def __init__(self, api_key: str) -> None:
        """Initialize the BaseWeatherAPIEndpoint."""
        self.query_params = {
            'key': api_key,
        }
        super().__init__()

    def _get_data(self, query_params: Optional[dict] = None) -> Any:
        """
        Get data from the API.

        Args:
            query_params (dict): The query parameters.

        Returns:
            Any: The data object from the API.
        """
        try:
            response = self._make_request(path=self.path, query_params=query_params)
        except (WeatherAPIRequestError, DataParserError) as error:
            raise WeatherAPIEndpointError(str(error))

        return self.data_parser(response.json()).data_to_object()


class WeatherEndpoint(BaseWeatherAPIEndpoint):
    """
    Represents the weather endpoint.

    Attributes:
        path (str): The path for the API.
        data_parser (BaseDataParser): The data parser for the API.
    """

    path: str = CURRENT_WEATHER_PATH
    data_parser: Type[BaseDataParser] = WeatherDataParser

    def get_current_weather(self, city_name: str) -> Any:
        """
        Get current weather data for a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            Any: The current weather data object for the city.
        """
        if not isinstance(city_name, str):
            raise WeatherAPIEndpointError('Invalid city type. Expected: str, got: {0}'.format(type(city_name)))
        if not city_name:
            raise WeatherAPIEndpointError('Argument city_name is required')
        query_params = {
            'q': city_name,
        }
        return self._get_data(query_params)


class ForecastEndpoint(BaseWeatherAPIEndpoint):
    """
    Represents the forecast endpoint.

    Attributes:
        path (str): The path for the API.
        data_parser (BaseDataParser): The data parser for the API.
    """

    path: str = FORECAST_PATH
    data_parser: Type[BaseDataParser] = ForecastDataParser

    def get_forecast(self, city_name: str) -> Any:
        """
        Get forecast data for a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            Any: The forecast data object for the city.
        """
        if not isinstance(city_name, str):
            raise WeatherAPIEndpointError('Invalid city type. Expected: str, got: {0}'.format(type(city_name)))
        if not city_name:
            raise WeatherAPIEndpointError('Argument city_name is required')
        query_params = {
            'q': city_name,
        }
        return self._get_data(query_params)
