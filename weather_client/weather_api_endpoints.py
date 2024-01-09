from weather_client.weather_api_requests import BaseWeatherAPIRequest
from weather_client.data_parsers import WeatherDataParser, ForecastDataParser, BaseDataParser
from weather_client.settings import BASE_URL, CURRENT_WEATHER_PATH, FORECAST_PATH
from weather_client.exceptions import WeatherAPIEndpointError, DataParserError, WeatherAPIRequestError


class BaseWeatherAPIEndpoint(BaseWeatherAPIRequest):
    BASE_URL = BASE_URL
    data_parser = BaseDataParser

    def __init__(self, api_key):
        self.query_params = {
            'key': api_key
        }
        super().__init__()

    def _get_data(self, query_params=None):
        try:
            response = self._make_request(path=self.PATH, query_params=query_params)
            data = response.json()
            obj = self.data_parser(data).data_to_object()
        except (WeatherAPIRequestError, DataParserError) as e:
            raise WeatherAPIEndpointError(str(e))

        return obj


class WeatherEndpoint(BaseWeatherAPIEndpoint):
    PATH = CURRENT_WEATHER_PATH
    data_parser = WeatherDataParser

    def get_current_weather(self, city_name):
        query_params = {
            'q': city_name,
        }
        return self._get_data(query_params)


class ForecastEndpoint(BaseWeatherAPIEndpoint):
    PATH = FORECAST_PATH
    data_parser = ForecastDataParser

    def get_forecast(self, city_name):
        query_params = {
            'q': city_name,
        }
        return self._get_data(query_params)
