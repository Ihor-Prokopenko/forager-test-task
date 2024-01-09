from weather_client.weather_api_endpoints import WeatherEndpoint, ForecastEndpoint
from weather_client.exceptions import WeatherAPIClientError, WeatherAPIEndpointError


class WeatherAPIClient(object):
    def __init__(self, api_key):
        self.WEATHER_API_KEY = api_key
        self.weather_endpoint = WeatherEndpoint
        self.forecast_endpoint = ForecastEndpoint

    def get_current_weather(self, city_name):
        weather_endpoint = self.weather_endpoint(self.WEATHER_API_KEY)
        try:
            obj = weather_endpoint.get_current_weather(city_name)
        except WeatherAPIEndpointError as e:
            raise WeatherAPIClientError(str(e))
        return obj

    def get_forecast(self, city_name):
        forecast_endpoint = self.forecast_endpoint(self.WEATHER_API_KEY)
        try:
            obj = forecast_endpoint.get_forecast(city_name)
        except WeatherAPIEndpointError as e:
            raise WeatherAPIClientError(str(e))
        return obj
