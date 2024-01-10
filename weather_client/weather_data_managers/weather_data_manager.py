"""Module providing weather-related functionality."""
from weather_client.exceptions import WeatherAPIClientError, WeatherAPIDataManagerError
from weather_client.weather_api_client import WeatherAPIClient
from weather_client.weather_data_classes import WeatherResult
from weather_client.weather_data_managers.base_data_manager import BaseDataManager


class WeatherResultManager(BaseDataManager):
    """
    Manages weather results.

    Attributes:
        data_class (type): The class used to store weather results.
    """

    data_class = WeatherResult

    def __init__(self, api_client: WeatherAPIClient) -> None:
        """Initialize the WeatherResultManager."""
        super().__init__(filter_field='city_name')
        self.objects_storage = []
        self._api_client = api_client

    def get(self, city_name: str = '') -> WeatherResult | list[WeatherResult]:
        """
        Get weather results for a specific city or all cities.

        Args:
            city_name (str): The name of the city.

        Returns:
            WeatherResult or list[WeatherResult]: Weather results for the specified city or all cities.
        """
        if not city_name:
            return self.objects_storage
        weather_obj = self._get_object(city_name)
        return weather_obj if weather_obj else []

    def request_and_save_weather(self, city_name: str) -> WeatherResult | None:
        """
        Get and save the current weather for the specified city.

        Args:
            city_name (str): The name of the city.

        Returns:
            WeatherResult: The current weather for the specified city.
        """
        client: WeatherAPIClient = self._api_client
        try:
            current_weather = client.weather.get_current_weather(city_name=city_name)
        except WeatherAPIClientError as error:
            raise WeatherAPIDataManagerError(str(error))
        return self.save(current_weather)

    def clear(self, city_name: str = '') -> int:
        """
        Clear weather results for a specific city or all cities.

        Args:
            city_name (str): The name of the city to clear results for.

        Returns:
            int: The number of deleted objects.
        """
        return self._delete_stored_objects(city_name)
