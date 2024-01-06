"""Module providing a service for interacting with the Weather API client."""
from weather_client.weather_client import WeatherAPIClient, WeatherResult


class WeatherServiceExceptionError(Exception):
    """Exception class for Weather Service-related errors."""


class WeatherResultManager(object):
    """
    Manages weather results.

    Attributes:
        _weather_results (list[WeatherResult]): A list of WeatherResult objects.
    """

    def __init__(self) -> None:
        """Initialize the WeatherResultManager."""
        self._weather_results: list[WeatherResult] = []

    def _save_or_update_weather_obj(self, result_obj: WeatherResult) -> WeatherResult:
        """
        Update or Save a WeatherResult object based on the given result object.

        Args:
            result_obj (WeatherResult): A WeatherResult object containing weather information for a city.

        Returns:
            WeatherResult: The WeatherResult object.
        """
        if not isinstance(result_obj, WeatherResult):
            raise WeatherServiceExceptionError('Invalid result type. Expected: WeatherResult')
        city_name = result_obj.city_name

        for weather_result_obj in self._weather_results:
            if weather_result_obj.city_name.lower() == city_name.lower():
                weather_result_obj.temperature = result_obj.temperature
                weather_result_obj.condition = result_obj.condition
                weather_result_obj.last_updated = result_obj.last_updated
                return weather_result_obj
        self._weather_results.append(result_obj)
        return result_obj

    def save_results(self, result_obj: WeatherResult | list[WeatherResult]) -> WeatherResult | list[WeatherResult]:
        """
        Save weather results in the WeatherResultManager.

        Args:
            result_obj (WeatherResult or list): Weather information for one or multiple cities.

        Returns:
            WeatherResult, list[WeatherResult], or None: Saved WeatherResult objects.
        """
        if not result_obj:
            return []
        if isinstance(result_obj, list):
            return_res: list[WeatherResult] = []
            for new_result in result_obj:
                new_obj: WeatherResult = self._save_or_update_weather_obj(new_result)
                return_res.append(new_obj)
            return return_res
        elif isinstance(result_obj, WeatherResult):
            return self._save_or_update_weather_obj(result_obj)

    def get_results(self, city_name: str = '') -> WeatherResult | list[WeatherResult]:
        """
        Get weather results for a specific city or all cities.

        Args:
            city_name (str): The name of the city.

        Returns:
            WeatherResult or list[WeatherResult]: Weather results for the specified city or all cities.
        """
        if not city_name:
            return self._weather_results
        return [result_obj for result_obj in self._weather_results if result_obj.city_name.lower() == city_name.lower()]

    def clear_results(self, city_name: str = '') -> bool:
        """
        Clear weather results for a specific city or all cities.

        Args:
            city_name (str): The name of the city to clear results for.

        Returns:
            bool: True if results were cleared successfully.
        """
        if not city_name:
            self._weather_results = []
            return True
        city_names = [weather_result.city_name.lower() for weather_result in self._weather_results]
        if city_name.lower() not in city_names:
            raise WeatherServiceExceptionError('City not found: {0}'.format(city_name))
        filtered_results = []
        for weather_result in self._weather_results:
            if weather_result.city_name.lower() != city_name.lower():
                filtered_results.append(weather_result)

        self._weather_results = filtered_results
        return True

    def get_results_count(self) -> int:
        """
        Get the count of stored weather results.

        Returns:
            int: The count of stored weather results.
        """
        return len(self._weather_results)

    def get_results_as_str(self) -> str:
        """
        Get a string representation of all stored weather results.

        Returns:
            str: String representation of all stored weather results.
        """
        return '\n'.join([str(result_obj) for result_obj in self._weather_results])


class WeatherService(WeatherResultManager):
    """
    Handles weather-related operations and results.

    Attributes:
        _api_client (WeatherAPIClient): An instance of the WeatherAPIClient class.
    """

    def __init__(self, api_client: WeatherAPIClient) -> None:
        """
        Initialize the WeatherService.

        Args:
            api_client: An instance of the WeatherAPIClient class.
        """
        super().__init__()
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

    def get_current_weather(self, city_name: str | list[str]) -> WeatherResult | list[WeatherResult]:
        """
        Get and save the current weather for one or multiple cities.

        Args:
            city_name (str or list[str]): The name of the city or a list of city names.

        Returns:
            WeatherResult or list[WeatherResult]: The current weather for the specified city or cities.
        """
        client: WeatherAPIClient = self._api_client
        if isinstance(city_name, list):
            return self.save_results([client.get_current_weather(city_name=city) for city in city_name])
        elif isinstance(city_name, str):
            return self.save_results(client.get_current_weather(city_name=city_name))
