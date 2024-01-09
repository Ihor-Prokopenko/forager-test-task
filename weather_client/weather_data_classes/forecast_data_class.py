"""Module providing weather-related functionality."""
from weather_client.weather_data_classes.base_data_class import BaseDataClass


class ForecastResult(BaseDataClass):
    """
    Represents the weather forecast result for a city.

    Attributes:
        city_name (str): The name of the city.
        avg_temp (float): The average temperature in Celsius.
        min_temp (float): The minimum temperature in Celsius.
        max_temp (float): The maximum temperature in Celsius.
        condition (str): The weather condition description.
        chance_of_rain (float): The chance of rain in percentage.
        chance_of_snow (float): The chance of snow in percentage.
        date (str): The date of the forecast.
    """

    def __init__(
            self,
            city_name: str,
            avg_temp: int | float,
            min_temp: int | float,
            max_temp: int | float,
            condition: str,
            chance_of_rain: int | float,
            chance_of_snow: int | float,
            date: str,
    ) -> None:
        """
        Initialize the WeatherResult.

        Args:
            city_name (str): The name of the city.
        """
        self.city_name = city_name
        self.avg_temp = avg_temp
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.condition = condition
        self.chance_of_rain = chance_of_rain
        self.chance_of_snow = chance_of_snow
        self.date = date

    def __str__(self) -> str:
        """Generate a string representation of the WeatherResult."""
        return 'City: {0}, Avg_temp: {1}, Condition: {2}, Date: {3}'.format(
            self.city_name,
            self.avg_temp,
            self.condition,
            self.date,
        )

    def __repr__(self) -> str:
        """Generate a string representation of the WeatherResult."""
        return 'object.ForecastResult(city_name={0}, date={1})'.format(self.city_name, self.date)
