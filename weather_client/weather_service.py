from weather_client.weather_client import WeatherAPIClient


class WeatherServiceException(Exception):
    pass


class WeatherResult:
    """
    Represents the weather result for a city.

    Attributes:
        city_name (str): The name of the city.
        temperature (float): The temperature in Celsius.
        condition (str): The weather condition description.
        last_updated (str): The timestamp of the last update.
    """
    def __init__(self, city_name: str, temperature: float, condition: str, last_updated: str):
        self.city_name = city_name
        self.temperature = temperature
        self.condition = condition
        self.last_updated = last_updated

    def __str__(self):
        return (f"City: {self.city_name}, Temp: {self.temperature}, "
                f"Condition: {self.condition}, Last Updated: {self.last_updated}")


class WeatherService:
    """
    Handles weather-related operations and results.

    Attributes:
        results (list[WeatherResult]): A list of WeatherResult objects.
        api_client (WeatherAPIClient): An instance of the WeatherAPIClient class.
    """
    def __init__(self):
        self.results = []
        self.api_client = WeatherAPIClient

    def _update_or_create_weather_obj(self, result: dict) -> WeatherResult:
        """
        Update or create a WeatherResult object based on the given result dictionary.

        Args:
            result (dict): A dictionary containing weather information for a city.

        Returns:
            WeatherResult: The WeatherResult object.
        """
        city_name = list(result.keys())[0]

        for existing_obj in self.results:
            if existing_obj.city_name.lower() == city_name.lower():
                existing_obj.temperature = result.get(city_name, {}).get("temperature")
                existing_obj.condition = result.get(city_name, {}).get("condition")
                existing_obj.last_updated = result.get(city_name, {}).get("last_updated")
                return existing_obj

        weather_obj = WeatherResult(
            city_name=city_name,
            temperature=result.get(city_name, {}).get("temperature"),
            condition=result.get(city_name, {}).get("condition"),
            last_updated=result.get(city_name, {}).get("last_updated")
        )
        self.results.append(weather_obj)
        return weather_obj

    def save_result(self, result: dict | list[dict]) -> WeatherResult | list[WeatherResult] | None:
        """
        Save weather results in the WeatherService.

        Args:
            result (dict or list): Weather information for one or multiple cities.

        Returns:
            WeatherResult, list[WeatherResult], or None: Saved WeatherResult objects.
        """
        if not result:
            return None
        if isinstance(result, list):
            return_res: list[WeatherResult] = []
            for item in result:
                new_obj: WeatherResult = self._update_or_create_weather_obj(item)
                return_res.append(new_obj)
            return return_res
        elif isinstance(result, dict):
            new_obj: WeatherResult = self._update_or_create_weather_obj(result)
            return new_obj
        else:
            raise WeatherServiceException(f"Invalid result type: {type(result)}. Must be dict or list[dict]")

    def get_results(self, city_name: str = None) -> WeatherResult | list[WeatherResult]:
        """
        Get weather results for a specific city or all cities.

        Args:
            city_name (str, optional): The name of the city.

        Returns:
            WeatherResult or list[WeatherResult]: Weather results for the specified city or all cities.
        """
        if city_name:
            return [result for result in self.results if result.city_name.lower() == city_name.lower()]
        return self.results

    def clear_results(self, city_name: str = None) -> bool:
        """
        Clear weather results for a specific city or all cities.

        Args:
            city_name (str, optional): The name of the city to clear results for.

        Returns:
            bool: True if results were cleared successfully.
        """
        if not city_name:
            self.results = []
            return True
        if not city_name.lower() in [result.city_name.lower() for result in self.results]:
            raise WeatherServiceException(f"City not found: {city_name}")
        self.results = [result for result in self.results if result.city_name.lower() != city_name.lower()]
        return True

    def get_results_count(self) -> int:
        """
        Get the count of stored weather results.

        Returns:
            int: The count of stored weather results.
        """
        return len(self.results)

    def get_results_as_str(self) -> str:
        """
        Get a string representation of all stored weather results.

        Returns:
            str: String representation of all stored weather results.
        """
        return "\n".join([str(result) for result in self.results])

    def get_current_weather(self, city_name: str | list[str], api_key: str) -> WeatherResult | list[WeatherResult]:
        """
        Get and save the current weather for one or multiple cities.

        Args:
            city_name (str or list[str]): The name of the city or a list of city names.
            api_key (str): The API key for accessing weather data.

        Returns:
            WeatherResult or list[WeatherResult]: The current weather for the specified city or cities.
        """
        client: WeatherAPIClient = self.api_client(api_key)
        if isinstance(city_name, list):
            weather: list[dict] = [client.get_current_weather(city_name=city) for city in city_name]
        elif isinstance(city_name, str):
            weather: dict = client.get_current_weather(city_name=city_name)
        else:
            raise WeatherServiceException(f"Invalid city_name type: {type(city_name)}. Must be str or list[str]")
        weather_obj: WeatherResult = self.save_result(weather)

        return weather_obj
