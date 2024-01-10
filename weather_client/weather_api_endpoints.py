"""Module providing weather-related functionality."""
from weather_client.data_parsers import WeatherDataParser, ForecastDataParser, BaseDataParser
from weather_client.exceptions import WeatherAPIEndpointError, DataParserError, WeatherAPIRequestError
from weather_client.settings import BASE_URL, CURRENT_WEATHER_PATH, FORECAST_PATH
from weather_client.weather_api_requests import BaseWeatherAPIRequest


class BaseWeatherAPIEndpoint(BaseWeatherAPIRequest):
    """
    Base class for weather API endpoints.

    Attributes:
        BASE_URL (str): The base URL for the API.
        PATH (str): The path for the API.
    """
    BASE_URL: str = BASE_URL
    data_parser: BaseDataParser = BaseDataParser

    def __init__(self, api_key: str) -> None:
        """Initialize the BaseWeatherAPIEndpoint."""
        self.query_params = {
            'key': api_key
        }
        super().__init__()

    def _get_data(self, query_params: dict = None) -> object:
        """
        Get data from the API.

        Args:
            query_params (dict): The query parameters.

        Returns:
            object: The data object from the API.
        """
        try:
            response = self._make_request(path=self.PATH, query_params=query_params)
            data = response.json()
            obj = self.data_parser(data).data_to_object()
        except (WeatherAPIRequestError, DataParserError) as e:
            raise WeatherAPIEndpointError(str(e))

        return obj


class WeatherEndpoint(BaseWeatherAPIEndpoint):
    """
    Represents the weather endpoint.

    Attributes:
        PATH (str): The path for the API.
        data_parser (BaseDataParser): The data parser for the API.
    """
    PATH: str = CURRENT_WEATHER_PATH
    data_parser: BaseDataParser = WeatherDataParser

    def get_current_weather(self, city_name: str) -> object:
        """
        Get current weather data for a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            object: The current weather data object for the city.
        """
        if not isinstance(city_name, str):
            raise WeatherAPIEndpointError('Invalid city type. Expected: str, got: {}'.format(type(city_name)))
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
        PATH (str): The path for the API.
        data_parser (BaseDataParser): The data parser for the API.
    """
    PATH: str = FORECAST_PATH
    data_parser: BaseDataParser = ForecastDataParser

    def get_forecast(self, city_name: str) -> object:
        """
        Get forecast data for a city.

        Args:
            city_name (str): The name of the city.

        Returns:
            object: The forecast data object for the city.
        """
        if not isinstance(city_name, str):
            raise WeatherAPIEndpointError('Invalid city type. Expected: str, got: {}'.format(type(city_name)))
        if not city_name:
            raise WeatherAPIEndpointError('Argument city_name is required')
        query_params = {
            'q': city_name,
        }
        return self._get_data(query_params)
