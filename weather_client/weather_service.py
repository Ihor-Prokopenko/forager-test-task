"""Module providing a service for interacting with the Weather API client."""
from weather_client.weather_client import WeatherAPIClient, WeatherResult


class WeatherServiceExceptionError(Exception):
    """Exception class for Weather Service-related errors."""

    pass  # NOQA


class WeatherService(object):
    """
    Handles weather-related operations and results.

    Attributes:
        _results (list[WeatherResult]): A list of WeatherResult objects.
        _api_client (WeatherAPIClient): An instance of the WeatherAPIClient class.
    """

    def __init__(self, api_client: WeatherAPIClient) -> None:
        """
        Initialize the WeatherService.

        Args:
            api_client: An instance of the WeatherAPIClient class.
        """
        self._results = []  # NOQA
        self._api_client = api_client

    @property
    def api_client(self):
        """Getter for the API client."""
        return self._api_client

    @api_client.setter
    def api_client(self, api_client):
        """Setter for the API client."""
        if not isinstance(api_client, WeatherAPIClient):
            raise WeatherServiceExceptionError('Invalid API client type. Expected: WeatherAPIClient')
        self._api_client = api_client

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

        existing_obj: list[WeatherResult] = [obj for obj in self._results if obj.city_name.lower() == city_name.lower()]  # NOQA
        if existing_obj:
            weather_result = existing_obj[0]
            weather_result.temperature = result_obj.temperature
            weather_result.condition = result_obj.condition
            weather_result.last_updated = result_obj.last_updated
            return weather_result
        self._results.append(result_obj)
        return result_obj

    def save_results(self, result_obj: WeatherResult | list[WeatherResult])\
            -> WeatherResult | list[WeatherResult] | None:
        """
        Save weather results in the WeatherService.

        Args:
            result_obj (dict or list): Weather information for one or multiple cities.

        Returns:
            WeatherResult, list[WeatherResult], or None: Saved WeatherResult objects.
        """
        if not result_obj:
            return None
        if isinstance(result_obj, list):
            return_res: list[WeatherResult] = []
            for new_result in result_obj:
                new_obj: WeatherResult = self._save_or_update_weather_obj(new_result)
                return_res.append(new_obj)
            return return_res
        elif isinstance(result_obj, WeatherResult):
            return self._save_or_update_weather_obj(result_obj)
        raise WeatherServiceExceptionError(f'Invalid result type: {type(result_obj)}. '      # NOQA
                                           f'Must be WeatherResult or list[WeatherResult]')  # NOQA

    def get_results(self, city_name: str = None) -> WeatherResult | list[WeatherResult]:
        """
        Get weather results for a specific city or all cities.

        Args:
            city_name (str, optional): The name of the city.

        Returns:
            WeatherResult or list[WeatherResult]: Weather results for the specified city or all cities.
        """
        if not city_name:
            return self._results
        return [result_obj for result_obj in self._results if result_obj.city_name.lower() == city_name.lower()]

    def clear_results(self, city_name: str = None) -> bool:
        """
        Clear weather results for a specific city or all cities.

        Args:
            city_name (str, optional): The name of the city to clear results for.

        Returns:
            bool: True if results were cleared successfully.
        """
        if not city_name:
            self._results = []  # NOQA
            return True
        if not city_name.lower() in [result.city_name.lower() for result in self._results]:  # NOQA
            raise WeatherServiceExceptionError(f'City not found: {city_name}')  # NOQA
        self._results = [result for result in self._results if result.city_name.lower() != city_name.lower()]  # NOQA
        return True

    def get_results_count(self) -> int:
        """
        Get the count of stored weather results.

        Returns:
            int: The count of stored weather results.
        """
        return len(self._results)

    def get_results_as_str(self) -> str:
        """
        Get a string representation of all stored weather results.

        Returns:
            str: String representation of all stored weather results.
        """
        return '\n'.join([str(result_obj) for result_obj in self._results])

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
            weather: list[WeatherResult] = [client.get_current_weather(city_name=city) for city in city_name]
        elif isinstance(city_name, str):
            weather: WeatherResult = client.get_current_weather(city_name=city_name)
        else:
            raise WeatherServiceExceptionError(f'Invalid city_name type: {type(city_name)}. '  # NOQA
                                               f'Must be str or list[str]')  # NOQA
        return self.save_results(weather)
