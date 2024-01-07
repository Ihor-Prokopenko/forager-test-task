"""Module providing weather-related functionality."""
from weather_data_classes import ForecastResult

from weather_client.exceptions import WeatherServiceExceptionError


class ForecastResultManager(object):
    """Manages weather forecast results."""

    _forecast_results: list[ForecastResult] = []

    def _save_or_update_forecast_obj(self, forecast_obj: ForecastResult) -> ForecastResult:
        """
        Update or Save a ForecastResult object based on the given result object.

        Args:
            forecast_obj (ForecastResult): A ForecastResult object containing weather forecast information for a city.

        Returns:
            ForecastResult: The ForecastResult object.
        """
        if not isinstance(forecast_obj, ForecastResult):
            raise WeatherServiceExceptionError('Invalid result type. Expected: ForecastResult')
        city_name = forecast_obj.city_name

        for existing_forecast_obj in self._forecast_results:
            if existing_forecast_obj.city_name.lower() == city_name.lower():
                existing_forecast_obj.avg_temp = forecast_obj.avg_temp
                existing_forecast_obj.min_temp = forecast_obj.min_temp
                existing_forecast_obj.max_temp = forecast_obj.max_temp
                existing_forecast_obj.condition = forecast_obj.condition
                existing_forecast_obj.chance_of_rain = forecast_obj.chance_of_rain
                existing_forecast_obj.chance_of_snow = forecast_obj.chance_of_snow
                existing_forecast_obj.date = forecast_obj.date
                return existing_forecast_obj
        self._forecast_results.append(forecast_obj)
        return forecast_obj

    def save_forecasts(
            self, forecast_obj: ForecastResult | list[ForecastResult],
    ) -> ForecastResult | list[ForecastResult]:
        """
        Save weather forecast results in the WeatherForecastResultManager.

        Args:
            forecast_obj (ForecastResult or list): Weather forecast information for one or multiple cities.

        Returns:
            ForecastResult, list[ForecastResult], or None: Saved ForecastResult objects.
        """
        if not forecast_obj:
            return []

        if isinstance(forecast_obj, list):
            return_res: list[ForecastResult] = []
            for new_forecast in forecast_obj:
                new_obj: ForecastResult = self._save_or_update_forecast_obj(new_forecast)
                return_res.append(new_obj)
            return return_res
        elif isinstance(forecast_obj, ForecastResult):
            return self._save_or_update_forecast_obj(forecast_obj)
        raise WeatherServiceExceptionError('Invalid result type. Expected: ForecastResult or list[ForecastResult]')

    def get_forecasts(self, city_name: str = '') -> ForecastResult | list[ForecastResult]:
        """
        Get weather forecast results for a specific city or all cities.

        Args:
            city_name (str): The name of the city.

        Returns:
            ForecastResult or list[ForecastResult]: The weather forecast results for the specified city or cities.
        """
        if not city_name:
            return self._forecast_results
        return [
            forecast for forecast in self._forecast_results if
            forecast.city_name.lower() == city_name.lower()
        ]

    def clear_forecasts(self, city_name: str = '') -> bool:
        """
        Clear weather forecast results for a specific city or all cities.

        Args:
            city_name (str): The name of the city.

        Returns:
            bool: True if the weather forecast results were cleared successfully, False otherwise.
        """
        if not city_name:
            self._forecast_results = []
            return True
        city_names = [forecast.city_name.lower() for forecast in self._forecast_results]
        if city_name.lower() not in city_names:
            raise WeatherServiceExceptionError('City not found: {0}'.format(city_name))
        filtered_forecasts = []
        for forecast in self._forecast_results:
            if forecast.city_name.lower() != city_name.lower():
                filtered_forecasts.append(forecast)
        self._forecast_results = filtered_forecasts
        return True

    def get_forecasts_count(self) -> int:
        """
        Get the count of stored weather forecast results.

        Returns:
            int: The count of stored weather forecast results.
        """
        return len(self._forecast_results)

    def get_forecasts_as_str(self) -> str:
        """
        Get weather forecast results as a string.

        Returns:
            str: The weather forecast results as a string.
        """
        return '\n'.join([str(forecast_obj) for forecast_obj in self._forecast_results])
