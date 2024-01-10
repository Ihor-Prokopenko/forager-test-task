"""Module providing weather-related functionality."""
from weather_client.weather_data_classes import ForecastResult
from weather_client.weather_data_managers.base_result_manager import BaseDataManager


class ForecastResultManager(BaseDataManager):
    """Manages weather forecast results."""
    data_class = ForecastResult

    def __init__(self) -> None:
        """
        Initialize the WeatherResultManager.
        """
        super().__init__(filter_field='city_name')
        self.objects_storage = []

    def get(self, city_name: str = '') -> ForecastResult | list[ForecastResult]:
        """
        Get weather forecast results for a specific city or all cities.

        Args:
            city_name (str): The name of the city.

        Returns:
            ForecastResult or list[ForecastResult]: The weather forecast results for the specified city or cities.
        """
        if not city_name:
            return self.objects_storage
        return self._get_object(city_name)

    def clear(self, city_name: str = '') -> int:
        """
        Clear forecast results for a specific city or all cities.

        Args:
            city_name (str): The name of the city to clear results for.

        Returns:
            int: The number of deleted objects.
        """
        return self._delete_stored_objects(city_name)
