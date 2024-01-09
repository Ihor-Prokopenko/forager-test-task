import requests
from weather_client.exceptions import WeatherAPIRequestError


class BaseWeatherAPIRequest(object):
    USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36")
    headers = {
        "User-Agent": USER_AGENT
    }
    BASE_URL = ''
    PATH = ""
    params = {}
    query_params = {}

    def __init__(self, base_url='', path='', headers=None, params=None, query_params=None):
        if base_url:
            self.BASE_URL = base_url
        if not base_url.endswith('/'):
            base_url += '/'
        if path:
            self.PATH = path
        if headers:
            headers.update(self.headers or {})
            self.headers = headers
        if params:
            params.update(self.params or {})
            self.params = params
        if query_params:
            query_params.update(self.query_params or {})
            self.query_params = query_params

    def _encode_query_params(self, query_params=None):
        params = ['{0}={1}'.format(key, value) for key, value in query_params.items()]
        return "&".join(params)

    def _build_url(self, path=None, query_params=None):
        if not query_params:
            return self.BASE_URL + path
        self.query_params.update(query_params)
        query_params = self._encode_query_params(self.query_params)
        if not path:
            return self.BASE_URL + "?" + query_params
        return self.BASE_URL + path + "?" + query_params

    def _make_request(self, path=None, query_params=None):
        url = self._build_url(path, query_params)
        response = requests.get(url, headers=self.headers, params=self.params, timeout=5)
        if response.status_code != requests.status_codes.codes.ok:
            message = response.json().get('error', {}).get('message')
            status_code = response.status_code
            raise WeatherAPIRequestError(message, status_code)
        return response
