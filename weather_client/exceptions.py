"""Module providing weather-related functionality."""


class WeatherServiceExceptionError(Exception):
    """Exception class for Weather Service-related errors."""


class WeatherAPIExceptionError(Exception):
    """Exception class for Weather API-related errors."""


class WeatherAPIRequestError(Exception):
    pass


class WeatherAPIEndpointError(Exception):
    pass


class WeatherAPIError(Exception):
    pass


class WeatherAPIClientError(Exception):
    pass


class DataParserError(Exception):
    pass

