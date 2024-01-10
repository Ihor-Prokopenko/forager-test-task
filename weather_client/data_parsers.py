"""Module providing weather-related functionality."""
from typing import Type

from weather_client.exceptions import DataParserError
from weather_client.weather_data_classes import BaseDataClass, ForecastResult, WeatherResult


class BaseDataParser(object):
    """
    Base class for data parsers.

    Attributes:
        data_class (BaseDataClass): The data class for the parser.
    """

    data_class: Type[BaseDataClass] = BaseDataClass

    def __init__(self, data_to_parse: dict) -> None:
        """Initialize the BaseDataParser."""
        self.data_to_parse = data_to_parse

    def _parse_data(self, data_to_parse: dict) -> dict:
        """
        Parse the data.

        Args:
            data_to_parse (dict): The data to parse.

        Returns:
            dict: The parsed data.
        """
        return data_to_parse

    def data_to_object(self) -> BaseDataClass:
        """
        Convert the data to an object.

        Returns:
            BaseDataClass: The object.
        """
        try:
            formatted_data = self._parse_data(self.data_to_parse)
        except TypeError as error:
            raise DataParserError(str(error))
        return self.data_class(**formatted_data)


class WeatherDataParser(BaseDataParser):
    """
    Data parser for weather data.

    Attributes:
        data_class (BaseDataClass): The data class for the parser.
    """

    data_class: Type[BaseDataClass] = WeatherResult

    def _parse_data(self, data_to_parse: dict) -> dict:
        """
        Parse the data.

        Args:
            data_to_parse (dict): The data to parse.

        Returns:
            dict: The parsed data.
        """
        if not isinstance(data_to_parse, dict):
            raise TypeError('Data must be a dictionary. Got {0}'.format(type(data_to_parse)))
        city_name = data_to_parse.get('location', {}).get('name', '')
        if not city_name:
            raise DataParserError('City name not found in data')
        return {
            'city_name': city_name,
            'temperature': data_to_parse.get('current', {}).get('temp_c', 0),
            'condition': data_to_parse.get('current', {}).get('condition', {}).get('text', ''),
            'last_updated': data_to_parse.get('current', {}).get('last_updated', ''),
        }


class ForecastDataParser(BaseDataParser):
    """
    Data parser for forecast data.

    Attributes:
        data_class (BaseDataClass): The data class for the parser.
    """

    data_class: Type[BaseDataClass] = ForecastResult

    def _parse_data(self, data_to_parse: dict) -> dict:
        """
        Parse the data.

        Args:
            data_to_parse (dict): The data to parse.

        Returns:
            dict: The parsed data.
        """
        if not isinstance(data_to_parse, dict):
            raise ValueError('Data must be a dictionary. Got {0}'.format(type(data_to_parse)))
        if not data_to_parse.get('location', {}).get('name'):
            raise DataParserError('City name not found in data')

        forecast_full_data = data_to_parse.get('forecast', {})
        forecastday = forecast_full_data.get('forecastday', [{}])[0]
        day_data = forecastday.get('day', {})
        day_condition = day_data.get('condition', {})

        return {
            'city_name': data_to_parse.get('location', {}).get('name', ''),
            'avg_temp': day_data.get('avgtemp_c', 0),
            'min_temp': day_data.get('mintemp_c', 0),
            'max_temp': day_data.get('maxtemp_c', 0),
            'condition': day_condition.get('text', ''),
            'chance_of_rain': day_data.get('daily_chance_of_rain', 0),
            'chance_of_snow': day_data.get('daily_chance_of_snow', 0),
            'date': forecastday.get('date', ''),
        }
