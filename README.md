#### Created by Ihor Prokopenko <i.prokopenko.dev@gmail.com>

# Weather Client Package
#### This Python package provides functionality to interact with the Weather API and manage weather-related information for various cities. 
#### The package consists of two main modules: weather_client.py for handling API requests, and weather_service.py for managing weather results.

## Installation
To install the package, use the following command:

```python
pip install git+https://github.com/Ihor-Prokopenko/forager-test-task.git
```

## Getting Started
### <span style="color:red">REQUIRED</span> :Before using the service, you need to create an account on [weatherapi.com](https://www.weatherapi.com/) and obtain an API key.

#### SignUp -> confirm email -> find api key in your [cabinet](https://www.weatherapi.com/my/)

#### There is a 1 million requests per month for FREE

***

## WeatherAPIClient Class
The WeatherAPIClient class allows you to connect to the Weather API and retrieve current weather data for a specific city.

Attributes:
- `_api_key (str)`: The API key for accessing the Weather API.

Public methods:
- `get_current_weather(city_name: str) -> WeatherResult`: Retrieves the current weather for a specific city.

Private methods:
- `_validate_api()`: Validates the connection to the Weather API.
- `_build_url(city_name: str = None) -> str`: Builds the full URL for the Weather API request.
- `_weather_data_to_object(data: dict) -> WeatherResult`: Creates a WeatherResult object based on weather data.

## Example using WeatherAPIClient:
```python
from weather_client import WeatherAPIClient

# Retrieve and set your api key
api_key = "your_weather_api_key"

# Create an instance of the WeatherAPIClient
client = WeatherAPIClient(api_key)

# Request the current weather for a specific city
weather_by_city_via_client = client.get_current_weather('London')
print(weather_by_city_via_client)
# City: London, Temp: 6.0, Condition: Partly cloudy, Last Updated: 2024-01-06 12:30
print(weather_by_city_via_client.city_name)
# London
print(weather_by_city_via_client.temperature)
# 6.0
print(weather_by_city_via_client.condition)
# Partly cloudy
print(weather_by_city_via_client.last_updated)
# 2024-01-06 12:30
```

***

## WeatherService Class

The WeatherService class manages weather-related operations and results. Retrieve current weather or specified one or multiple cities as well.

Attributes:

- `_results (list[WeatherResult])`: A list of WeatherResult objects.
- `_api_client (WeatherAPIClient)`: An instance of the WeatherAPIClient class.

Public methods:

- `save_results(self, result: WeatherResult | list[WeatherResult]) -> WeatherResult | list[WeatherResult] | None`: Saves weather results in the WeatherService.
- `get_results(city_name: str = None) -> WeatherResult | list[WeatherResult]`: Gets weather results for a specific city or all cities.
- `clear_results(city_name: str = None) -> bool`: Clears weather results for a specific city or all cities.
- `get_results_count() -> int`: Gets the count of stored weather results.
- `get_results_as_str() -> str`: Gets a string representation of all stored weather results.
- `get_current_weather(city_name: str | list[str], api_key: str) -> WeatherResult | list[WeatherResult]`: Gets and saves the current weather for one or multiple cities.

Private methods:
- `_save_or_update_weather_obj(self, result: WeatherResult) -> WeatherResult`: Update or Save a WeatherResult object based on the given result object.

## Example using WeatherService:
```python
from weather_client import WeatherAPIClient, WeatherService

api_key = "your_weather_api_key"

"""Create an instance of the WeatherAPIClient class"""
client = WeatherAPIClient(api_key)

"""Request the current weather for a specific city via WeatherAPIClient"""
weather_by_city_via_client = client.get_current_weather('London')
print(weather_by_city_via_client)
# City: London, Temp: 6.0, Condition: Partly cloudy, Last Updated: 2024-01-06 12:30

"""Create an instance of the WeatherService class"""
service = WeatherService(client)

"""Save the current weather for a specific city"""
saved = service.save_results(weather_by_city_via_client)
print(saved)
# City: London, Temp: 6.0, Condition: Partly cloudy, Last Updated: 2024-01-06 12:30

"""Get stored results for a specific city or all stored cities"""
saved_results = service.get_results()
print(saved_results)
# [<weather_client.weather_client.WeatherResult object at 0x7f0d4abe5410>,
# <weather_client.weather_client.WeatherResult object at 0x7f0d4ab4eed0>]

"""Get current weather results for a specific city, cities list"""
cities = ['london', 'Paris']
results = service.get_current_weather(cities)
print(results)
# [<weather_client.weather_client.WeatherResult object at 0x7f0d4abe5410>,
# <weather_client.weather_client.WeatherResult object at 0x7f0d4ab4eed0>]


"""Clear weather results for a specific city or all stored cities"""
deleted = service.clear_results('london')
print(deleted)
# True


"""Get the count of stored weather results"""
print(service.get_results_count())
# 1


"""Get a string representation of all stored weather results"""
results_str = service.get_results_as_str()
print(results_str)
# City: Paris, Temp: 7.0, Condition: Overcast, Last Updated: 2024-01-06 13:00
```

***

## WeatherResult class

The WeatherResult class represents the weather result for a city.

Attributes:
- `city_name (str)`: The name of the city.
- `temperature (float)`: The temperature in Celsius.
- `condition (str)`: The weather condition description.
- `last_updated (str)`: The timestamp of the last update.

Methods:
- `__init__(self, city_name: str, temperature: int | float, condition: str, last_updated: str) -> None`: Initialize the WeatherResult class.

Args:
- `city_name (str)`: The name of the city.
- `temperature (int | float)`: The temperature in Celsius.
- `condition (str)`: The weather condition description.
- `last_updated (str)`: The timestamp of the last update.

## Example:
```python
from weather_client import WeatherResult

# Create an instance of the WeatherResult class
result = WeatherResult(city_name='London', temperature=6.0, condition='Partly cloudy', last_updated='2024-01-06 12:30')

# Print the string representation of the WeatherResult
print(result)
# City: London, Temp: 6.0, Condition: Partly cloudy, Last Updated: 2024-01-06 12:30

```

***

## Conclusion
Feel free to use and extend this package to suit your weather-related needs. If you encounter any issues, please refer to the WeatherAPIException and WeatherServiceException classes for error handling.
