"""Module providing weather-related functionality."""
from weather_client.exceptions import WeatherAPIClientError, WeatherAPIDataManagerError
from weather_client.weather_api_client import WeatherAPIClient
from weather_client.weather_data_classes import ForecastResult
from weather_client.weather_data_managers.base_data_manager import BaseDataManager


class ForecastResultManager(BaseDataManager):
    """Manages weather forecast results."""

    data_class = ForecastResult

    def __init__(self, api_client: WeatherAPIClient) -> None:
        """Initialize the WeatherResultManager."""
        super().__init__(filter_field='city_name')
        self.objects_storage = []
        self._api_client = api_client

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
        forecast_obj = self._get_object(city_name)
        return forecast_obj if forecast_obj else []

    def request_and_save_forecast(self, city_name: str) -> ForecastResult | None:
        """
        Get and save the forecast for the specified city.

        Args:
            city_name (str): The name of the city.

        Returns:
            ForecastResult: The forecast for the specified city.
        """
        client: WeatherAPIClient = self._api_client
        try:
            forecast = client.forecast.get_forecast(city_name=city_name)
        except WeatherAPIClientError as error:
            raise WeatherAPIDataManagerError(str(error))
        return self.save(forecast)

    def clear(self, city_name: str = '') -> int:
        """
        Clear forecast results for a specific city or all cities.

        Args:
            city_name (str): The name of the city to clear results for.

        Returns:
            int: The number of deleted objects.
        """
        return self._delete_stored_objects(city_name)
