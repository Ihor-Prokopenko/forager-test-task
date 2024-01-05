# Weather Client Package
#### This Python package provides functionality to interact with the Weather API and manage weather-related information for various cities. 
#### The package consists of two main modules: weather_client.py for handling API requests, and weather_service.py for managing weather results.

## Installation
To install the package, use the following command:

- ```pip install git+https://github.com/Ihor-Prokopenko/forager-test-task.git```

## Getting Started
### Before using the service, you need to create an account on [weatherapi.com](https://www.weatherapi.com/) and obtain an API key.

SignUp -> confirm email -> find api key in your [cabinet](https://www.weatherapi.com/my/)

#### There is a 1 million requests per month for FREE

## WeatherAPIClient Class
The WeatherAPIClient class allows you to connect to the Weather API and retrieve current weather data for a specific city.

Attributes:
- api_key (str): The API key for accessing the Weather API.

Public methods:
- `get_current_weather(city_name: str) -> dict`: Retrieves the current weather for a specific city.

Private methods:
- `_validate_api()`: Validates the connection to the Weather API.
- `_build_url(city_name: str = None) -> str`: Builds the full URL for the Weather API request.
- `_format_weather_data(data: dict) -> dict`: Formats raw weather data from the API response.

## Example using WeatherAPIClient
```python
from weather_client import WeatherAPIClient

# Creating an instance of the WeatherAPIClient class
api_key = "your_weather_api_key"
weather_client = WeatherAPIClient(api_key)

# Getting current weather for a specific city
current_weather = weather_client.get_current_weather(city_name="London")
print(current_weather)

### {'London': {'temperature': 44.6, 'condition': 'Light rain', 'last_updated': '2024-01-05 18:30'}}
```

## WeatherService Class

The WeatherService class manages weather-related operations and results. Retrieve current weather or specified one or multiple cities as well.

Attributes:

- results (list[WeatherResult]): A list of WeatherResult objects.
- api_client (WeatherAPIClient): An instance of the WeatherAPIClient class.

Public methods:

- `save_result(result: dict | list[dict]) -> WeatherResult | list[WeatherResult] | None`: Saves weather results in the WeatherService.
- `get_results(city_name: str = None) -> WeatherResult | list[WeatherResult]`: Gets weather results for a specific city or all cities.
- `clear_results(city_name: str = None) -> bool`: Clears weather results for a specific city or all cities.
- `get_results_count() -> int`: Gets the count of stored weather results.
- `get_results_as_str() -> str`: Gets a string representation of all stored weather results.
- `get_current_weather(city_name: str | list[str], api_key: str) -> WeatherResult | list[WeatherResult]`: Gets and saves the current weather for one or multiple cities.

Private methods:
- `_update_or_create_weather_obj(result: dict) -> WeatherResult`: Updates or creates a WeatherResult object based on the given result dictionary.

## Example using WeatherService
```python
from weather_client import WeatherAPIClient, WeatherService

api_key = "your_weather_api_key"
# Creating an instance of the WeatherAPIClient class
weather_client = WeatherAPIClient(api_key)

# Creating an instance of the WeatherService class
weather_service = WeatherService()

# Getting current weather for a specific city
weather_data = weather_client.get_current_weather(city_name="London")

saved_results = weather_service.save_result(weather_data)
print("Saved Weather Results:", saved_results)
#>>> Saved Weather Results: City: London, Temp: 44.6, Condition: Light rain, Last Updated: 2024-01-05 18:30

# Getting results for a specific city
results_for_london = weather_service.get_results(city_name="London")
print("Weather Results for London:", results_for_london)
#>>> Weather Results for London: [<weather_client.weather_service.WeatherResult object at 0x7f350a926f10>]

# Number of saved results
results_count = weather_service.get_results_count()
print("Number of Saved Weather Results:", results_count)
#>>> Number of Saved Weather Results: 1

# String representation of all saved results
results_str = weather_service.get_results_as_str()
print("String Representation of Weather Results:", results_str)
#>>> String Repr. of Weather Results: City: London, Temp: 44.6, Condition: Light rain, Last Updated: 2024-01-05 18:30

# Clearing results for a specific city
success = weather_service.clear_results(city_name="London")
print(success)
#>>> True

"""Also, You can request weather for the one or many cities by using get_current_weather() method of WeatherService"""

cities_to_check = ["London", "Paris", "Kyiv"]

weather_results = weather_service.get_current_weather(cities_to_check, api_key)
print(weather_results)
#[<weather_client.weather_service.WeatherResult object at 0x7f9e0e73e450>, 
# <weather_client.weather_service.WeatherResult object at 0x7f9e0e6b41d0>, 
# <weather_client.weather_service.WeatherResult object at 0x7f9e0e73e310>]

print(weather_service.get_results_as_str())
# City: London, Temp: 44.6, Condition: Light rain, Last Updated: 2024-01-05 18:45
# City: Paris, Temp: 42.8, Condition: Clear, Last Updated: 2024-01-05 19:45
# City: Kyiv, Temp: 25.2, Condition: Clear, Last Updated: 2024-01-05 20:45

```

Feel free to use and extend this package to suit your weather-related needs. If you encounter any issues, please refer to the WeatherAPIException and WeatherServiceException classes for error handling.