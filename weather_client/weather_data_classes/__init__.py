"""Module providing weather-related functionality."""
from weather_client.weather_data_classes.base_data_class import BaseDataClass
from weather_client.weather_data_classes.forecast_data_class import ForecastResult
from weather_client.weather_data_classes.weather_data_class import WeatherResult

__all__ = [
    'WeatherResult',
    'ForecastResult',
    'BaseDataClass',
]
