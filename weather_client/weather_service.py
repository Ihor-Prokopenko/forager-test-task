"""Module providing a service for interacting with the Weather API client."""
from weather_client.exceptions import WeatherServiceExceptionError
from weather_client.weather_api_client import WeatherAPIClient
from weather_client.weather_data_classes import ForecastResult, WeatherResult
from weather_client.weather_data_managers import ForecastResultManager, WeatherResultManager


class WeatherService(WeatherResultManager, ForecastResultManager):
    """
    Handles weather-related operations and results.

    Attributes:
        _api_client (WeatherAPIClient): An instance of the WeatherAPIClient class.

    Methods:
        request_current_weather(city_name): Gets and saves the current weather for one or multiple cities.
        request_forecast(city_name): Gets and saves the forecast for one or multiple cities.
        save_weather(weather_obj): Saves weather results in the WeatherService.
        save_forecasts(forecast_obj): Saves forecast results in the WeatherService.
        get_weather(city_name): Gets weather results for a specific city or all cities.
        get_forecast(city_name): Gets forecast results for a specific city or all cities.
        clear_weather(city_name): Clears weather results for a specific city or all cities.
        clear_forecast(city_name): Clears forecast results for a specific city or all cities.
    """

    def __init__(self, api_client: WeatherAPIClient) -> None:
        """
        Initialize the WeatherService.

        Args:
            api_client: An instance of the WeatherAPIClient class.
        """
        self._api_client = api_client

    @property
    def api_client(self) -> WeatherAPIClient:
        """Getter for the API client."""
        return self._api_client

    @api_client.setter
    def api_client(self, api_client: WeatherAPIClient) -> None:
        """Setter for the API client."""
        if not isinstance(api_client, WeatherAPIClient):
            raise WeatherServiceExceptionError('Invalid API client type. Expected: WeatherAPIClient')
        self._api_client = api_client

    def request_current_weather(self, city_name: str | list[str]) -> WeatherResult | list[WeatherResult]:
        """
        Get and save the current weather for one or multiple cities.

        Args:
            city_name (str or list[str]): The name of the city or a list of city names.

        Returns:
            WeatherResult or list[WeatherResult]: The current weather for the specified city or cities.
        """
        if not city_name:
            return []

        client: WeatherAPIClient = self._api_client
        if isinstance(city_name, list):
            current_weather_list: list[WeatherResult] = []
            for city in city_name:
                if not isinstance(city, str):
                    raise WeatherServiceExceptionError('Invalid city type. Expected: str')
                current_weather = client.request_current_weather(city_name=city)
                if not current_weather:
                    continue
                current_weather_list.append(current_weather)
            return self.save_weather(current_weather_list)

        elif isinstance(city_name, str):
            current_weather = client.request_current_weather(city_name=city_name)
            if not current_weather:
                return []
            return self.save_weather(current_weather)

    def request_forecast(self, city_name: str | list[str]) -> ForecastResult | list[ForecastResult]:
        """
        Get and save the forecast for one or multiple cities.

        Args:
            city_name (str or list[str]): The name of the city or a list of city names.

        Returns:
            ForecastResult or list[ForecastResult]: The forecast for the specified city or cities.
        """
        if not city_name:
            return []

        client: WeatherAPIClient = self._api_client
        if isinstance(city_name, list):
            forecast_list: list[ForecastResult] = []
            for city in city_name:
                if not isinstance(city, str):
                    raise WeatherServiceExceptionError('Invalid city type. Expected: str')
                forecast = client.request_forecast(city_name=city)
                if not forecast:
                    continue
                forecast_list.append(forecast)
            return self.save_forecasts(forecast_list)

        elif isinstance(city_name, str):
            forecast = client.request_forecast(city_name=city_name)
            if not forecast:
                return []
            return self.save_forecasts(forecast)
