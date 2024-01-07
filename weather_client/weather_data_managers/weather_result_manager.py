"""Module providing weather-related functionality."""
from weather_client.exceptions import WeatherServiceExceptionError
from weather_client.weather_data_classes import WeatherResult


class WeatherResultManager(object):
    """
    Manages weather results.

    Attributes:
        _weather_results (list[WeatherResult]): A list of WeatherResult objects.
    """

    _weather_results: list[WeatherResult] = []

    def _save_or_update_weather_obj(self, weather_obj: WeatherResult) -> WeatherResult:
        """
        Update or Save a WeatherResult object based on the given result object.

        Args:
            weather_obj (WeatherResult): A WeatherResult object containing weather information for a city.

        Returns:
            WeatherResult: The WeatherResult object.
        """
        if not isinstance(weather_obj, WeatherResult):
            raise WeatherServiceExceptionError('Invalid result type. Expected: WeatherResult')
        city_name = weather_obj.city_name

        for weather_result_obj in self._weather_results:
            if weather_result_obj.city_name.lower() == city_name.lower():
                weather_result_obj.temperature = weather_obj.temperature
                weather_result_obj.condition = weather_obj.condition
                weather_result_obj.last_updated = weather_obj.last_updated
                return weather_result_obj
        self._weather_results.append(weather_obj)
        return weather_obj

    def save_weather(self, weather_obj: WeatherResult | list[WeatherResult]) -> WeatherResult | list[WeatherResult]:
        """
        Save weather results in the WeatherResultManager.

        Args:
            weather_obj (WeatherResult or list): Weather information for one or multiple cities.

        Returns:
            WeatherResult, list[WeatherResult], or None: Saved WeatherResult objects.
        """
        if not weather_obj:
            return []
        if isinstance(weather_obj, list):
            return_res: list[WeatherResult] = []
            for new_result in weather_obj:
                new_obj: WeatherResult = self._save_or_update_weather_obj(new_result)
                return_res.append(new_obj)
            return return_res
        elif isinstance(weather_obj, WeatherResult):
            return self._save_or_update_weather_obj(weather_obj)
        raise WeatherServiceExceptionError('Invalid result type. Expected: WeatherResult or list[WeatherResult]')

    def get_weather(self, city_name: str = '') -> WeatherResult | list[WeatherResult]:
        """
        Get weather results for a specific city or all cities.

        Args:
            city_name (str): The name of the city.

        Returns:
            WeatherResult or list[WeatherResult]: Weather results for the specified city or all cities.
        """
        if not city_name:
            return self._weather_results
        return [
            weather_obj for weather_obj in self._weather_results if
            weather_obj.city_name.lower() == city_name.lower()
        ]

    def clear_weather(self, city_name: str = '') -> bool:
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

    def get_weather_count(self) -> int:
        """
        Get the count of stored weather results.

        Returns:
            int: The count of stored weather results.
        """
        return len(self._weather_results)

    def get_weather_as_str(self) -> str:
        """
        Get a string representation of all stored weather results.

        Returns:
            str: String representation of all stored weather results.
        """
        return '\n'.join([str(weather_obj) for weather_obj in self._weather_results])
