from weather_client.exceptions import DataParserError
from weather_client.weather_data_classes import ForecastResult, WeatherResult, BaseDataClass


class BaseDataParser(object):
    """
    Base class for data parsers.

    Attributes:
        data_class (BaseDataClass): The data class for the parser.
    """
    data_class = BaseDataClass

    def __init__(self, data: dict) -> None:
        """Initialize the BaseDataParser."""
        self.data = data

    def _parse_data(self, data: dict) -> dict:
        """
        Parse the data.

        Args:
            data (dict): The data to parse.

        Returns:
            dict: The parsed data.
        """
        return data

    def data_to_object(self) -> object:
        """
        Convert the data to an object.

        Returns:
            object: The object.
        """
        try:
            formatted_data = self._parse_data(self.data)
            obj = self.data_class(**formatted_data)
        except TypeError as e:
            raise DataParserError(str(e))
        return obj


class WeatherDataParser(BaseDataParser):
    """
    Data parser for weather data.

    Attributes:
        data_class (BaseDataClass): The data class for the parser.
    """
    data_class: BaseDataClass = WeatherResult

    def _parse_data(self, data: dict) -> dict:
        """
        Parse the data.

        Args:
            data (dict): The data to parse.

        Returns:
            dict: The parsed data.
        """
        if not isinstance(data, dict):
            raise TypeError('Data must be a dictionary. Got {0}'.format(type(data)))
        city_name = data.get('location', {}).get('name', '')
        if not city_name:
            raise DataParserError('City name not found in data')
        formatted_data = {
            'city_name': city_name,
            'temperature': data.get('current', {}).get('temp_c', 0),
            'condition': data.get('current', {}).get('condition', {}).get('text', ''),
            'last_updated': data.get('current', {}).get('last_updated', ''),
        }
        return formatted_data


class ForecastDataParser(BaseDataParser):
    """
    Data parser for forecast data.

    Attributes:
        data_class (BaseDataClass): The data class for the parser.
    """
    data_class: BaseDataClass = ForecastResult

    def _parse_data(self, data: dict) -> dict:
        """
        Parse the data.

        Args:
            data (dict): The data to parse.

        Returns:
            dict: The parsed data.
        """
        if not isinstance(data, dict):
            raise ValueError('Data must be a dictionary. Got {0}'.format(type(data)))
        if not data.get('location', {}).get('name'):
            raise DataParserError('City name not found in data')

        forecast_full_data = data.get('forecast', {})
        forecastday = forecast_full_data.get('forecastday', [{}])[0]
        day_data = forecastday.get('day', {})
        day_condition = day_data.get('condition', {})

        formatted_data = {
            'city_name': data.get('location', {}).get('name', ''),
            'avg_temp': day_data.get('avgtemp_c', 0),
            'min_temp': day_data.get('mintemp_c', 0),
            'max_temp': day_data.get('maxtemp_c', 0),
            'condition': day_condition.get('text', ''),
            'chance_of_rain': day_data.get('daily_chance_of_rain', 0),
            'chance_of_snow': day_data.get('daily_chance_of_snow', 0),
            'date': forecastday.get('date', ''),
        }
        return formatted_data
