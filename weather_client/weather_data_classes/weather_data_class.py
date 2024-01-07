"""Module providing weather-related functionality."""


class WeatherResult(object):
    """
    Represents the weather result for a city.

    Attributes:
        city_name (str): The name of the city.
        temperature (float): The temperature in Celsius.
        condition (str): The weather condition description.
        last_updated (str): The timestamp of the last update.
    """

    def __init__(self, city_name: str, temperature: int | float, condition: str, last_updated: str) -> None:
        """
        Initialize the WeatherResult.

        Args:
            city_name (str): The name of the city.
            temperature (int | float): The temperature in Celsius.
            condition (str): The weather condition description.
            last_updated (str): The timestamp of the last update.
        """
        self.city_name = city_name
        self.temperature = temperature
        self.condition = condition
        self.last_updated = last_updated

    def __str__(self) -> str:
        """Generate a string representation of the WeatherResult."""
        return 'City: {0}, Temp: {1}, Condition: {2}, Last Updated: {3}'.format(
            self.city_name,
            self.temperature,
            self.condition,
            self.last_updated,
        )

    def __repr__(self) -> str:
        """Generate a string representation of the WeatherResult."""
        return 'object.WeatherResult(city_name={0})'.format(self.city_name)
