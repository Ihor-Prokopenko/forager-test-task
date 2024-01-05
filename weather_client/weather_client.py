import requests
from urllib.parse import urljoin, urlencode

BASE_URL = "https://api.weatherapi.com/"
WEATHER_API_PATH = "v1/current.json"


class WeatherAPIException(Exception):
    pass


class WeatherAPIClient(object):
    def __init__(self, api_key, base_url=BASE_URL, api_path=WEATHER_API_PATH):
        self.api_key = api_key
        self.base_url = base_url
        self.api_path = api_path
        self._validate_api()

    def _validate_api(self):
        response = requests.get(self.base_url)
        if not response.status_code == 200:
            raise WeatherAPIException(f"Failed to connect to Weather API. "
                                      f"Status code: {response.status_code}")

    def _build_url(self, city_name: str = None) -> str:
        full_url = urljoin(self.base_url, self.api_path)

        params = {"key": self.api_key}
        if city_name:
            params["q"] = city_name

        full_url += "?" + urlencode(params)
        return full_url

    @staticmethod
    def _format_weather_data(data: dict) -> dict:
        formatted_data = {
            data.get("location", {}).get("name"): {
                "temperature": data.get("current", {}).get("temp_f"),
                "condition": data.get("current", {}).get("condition", {}).get("text"),
                "last_updated": data.get("current", {}).get("last_updated"),
            }
        }
        return formatted_data

    def get_current_weather(self, city_name: str = None):
        url = self._build_url(city_name)
        response = requests.get(url)
        if not response.status_code == 200:
            raise WeatherAPIException(f"{response.json().get('error', {}).get('message')} "
                                      f"Status code: {response.status_code}")

        return self._format_weather_data(response.json())
