"""Module providing weather-related functionality."""
from weather_data_classes import ForecastResult, WeatherResult


class DataParserMixin(object):
    """
    Parses weather data from the Weather API response and creates objects.

    Attributes:
        _weather_data_class (type): The class for the weather data.
        _forecast_data_class (type): The class for the forecast data.

    Methods:
        _weather_data_to_object(self, weather_data: dict)
        _forecast_data_to_object(self, forecast_data: dict)
    """

    _weather_data_class = WeatherResult
    _forecast_data_class = ForecastResult

    def _weather_data_to_object(self, weather_data: dict) -> WeatherResult | None:
        """
        Create a WeatherResult object based on weather data.

        Args:
            weather_data (dict): The weather data to parse.

        Returns:
            WeatherResult: A WeatherResult object.
        """
        city_name = weather_data.get('location', {}).get('name')
        if not city_name:
            return None
        formatted_data = {
            'city_name': city_name,
            'temperature': weather_data.get('current', {}).get('temp_c'),
            'condition': weather_data.get('current', {}).get('condition', {}).get('text'),
            'last_updated': weather_data.get('current', {}).get('last_updated'),
        }
        return self._weather_data_class(**formatted_data)

    def _forecast_data_to_object(self, forecast_data: dict) -> ForecastResult | None:
        """
        Create a ForecastResult object based on forecast data.

        Args:
            forecast_data (dict): The forecast data to parse.

        Returns:
            ForecastResult: A ForecastResult object.
        """
        if not forecast_data.get('location', {}).get('name'):
            return None
        forecast_full_data = forecast_data.get('forecast', {})
        forecastday = forecast_full_data.get('forecastday', [{}])[0]
        day_data = forecastday.get('day', {})
        day_condition = day_data.get('condition', {})

        formatted_data = {
            'city_name': forecast_data.get('location', {}).get('name'),
            'avg_temp': day_data.get('avgtemp_c'),
            'min_temp': day_data.get('mintemp_c'),
            'max_temp': day_data.get('maxtemp_c'),
            'condition': day_condition.get('text'),
            'chance_of_rain': day_data.get('daily_chance_of_rain'),
            'chance_of_snow': day_data.get('daily_chance_of_snow'),
            'date': forecastday.get('date'),
        }
        return self._forecast_data_class(**formatted_data)
