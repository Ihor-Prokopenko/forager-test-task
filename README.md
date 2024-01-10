#### Created by Ihor Prokopenko <i.prokopenko.dev@gmail.com>

# Weather Client Package
#### This Python package provides functionality to interact with the Weather API and manage weather-related information for various cities. 
#### The package consists of two main modules: weather_client.py for handling API requests, and weather_service.py for managing weather results.


## Installation
To install the package, use the following command:

- ```pip install git+https://github.com/Ihor-Prokopenko/forager-test-task.git```

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
- `get_current_weather(city_name: str)`: Request the current weather for a specific city.
- `get_forecast(city_name: str)`: Request the forecast for a specific city.


## Example using WeatherAPIClient:
```python
from weather_client import WeatherAPIClient

# >>>> Retrieve and set your api key <<<<
api_key = "your_weather_api_key"

# >>>> create an instance of the CLIENT <<<<
client = WeatherAPIClient(api_key)

# >>>> request weather by city name via CLIENT <<<
weather_in_london = client.weather.get_current_weather('London')
print(weather_in_london)
# City: London, Temp: 2.0, Condition: Clear, Last Updated: 2024-01-09 23:30
print(weather_in_london.condition)
# Clear
print(weather_in_london.temperature)
# 4.0

# >>>> request weather forecast by city name via CLIENT <<<<
forecast_for_london = client.forecast.get_forecast('London')
print(forecast_for_london)
# City: London, Avg_temp: 2.0, Condition: Partly cloudy, Date: 2024-01-09
print(forecast_for_london.avg_temp)
# 2.0
print(forecast_for_london.date)
# 2024-01-09
print(forecast_for_london.condition)
# Partly cloudy
```

***

## WeatherService Class

The WeatherService class manages weather-related operations and results. Retrieve current weather of specified city as well.

Attributes:

- `weather_data`: WeatherResultManager()
- `forecast_data`: ForecastResultManager()

Managers methods:

  - `client.weather_data.request_and_save_weather(city_name: str)`: Get and save the current weather for the specified city.
  - `client.forecast_data.request_and_save_forecast(city_name: str)`: Get and save the forecast for the specified city.

  - `data_manager.save(filter_field_value: str)`: Store result.
  - `data_manager.get(filter_field_value:str)`: Get the specified object from the storage by specific field value.
  - `data_manager.clear(filter_field_value: str)`: Delete specified or all data objects from storage.
  - `data_manager.count()`: Get the count of stored data objects results.
  - `data_manager.get_as_str()`: Get the stored object as a string.


## Example using WeatherService:
```python
from weather_client import WeatherAPIClient, WeatherService

api_key = "your_weather_api_key"

# >>>> create an instance of the CLIENT <<<<
client = WeatherAPIClient(api_key)
weather_in_london = client.weather.get_current_weather('London')
forecast_for_london = client.forecast.get_forecast('London')

# >>>> create an instance of the SERVICE <<<<
service = WeatherService(client)


# >>>> save the results via SERVICE <<<<
saved_forecast = service.forecast_data.save(forecast_for_london)
saved_weather = service.weather_data.save(weather_in_london)
print(saved_forecast)
# City: London, Avg_temp: 2.0, Condition: Partly cloudy, Date: 2024-01-09
print(saved_weather)
# City: London, Temp: 2.0, Condition: Clear, Last Updated: 2024-01-09 23:30


# >>>> request and save weather and forecast by city name via SERVICE <<<<
city = 'Paris'
service.forecast_data.request_and_save_forecast(city)
service.weather_data.request_and_save_weather(city)

print(service.forecast_data.get())
# [object.ForecastResult(city_name=London, date=2024-01-09), object.ForecastResult(city_name=Paris, date=2024-01-10)]
print(service.weather_data.get())
# [object.WeatherResult(city_name=London), object.WeatherResult(city_name=Paris)]


# >>>> get the count of stored results <<<<
print(service.weather_data.count())
# 2
print(service.forecast_data.count())
# 2


# >>>> get the results as a string <<<<
print(service.weather_data.get_as_str())
# City: London, Temp: 2.0, Condition: Clear, Last Updated: 2024-01-09 23:30
# City: Paris, Temp: -2.0, Condition: Overcast, Last Updated: 2024-01-10 00:30
print(service.forecast_data.get_as_str())
# City: London, Avg_temp: 2.0, Condition: Partly cloudy, Date: 2024-01-09
# City: Paris, Avg_temp: -0.5, Condition: Partly cloudy, Date: 2024-01-10


# >>>> deletion results for specific or all cities <<<<
num_deleted = service.forecast_data.clear('London')
print(num_deleted)
# 1
print(service.forecast_data.get())
# [object.ForecastResult(city_name=Paris, date=2024-01-10)]

service.weather_data.clear()
print(service.weather_data.get())
# []
```

***

***

## Conclusion
Feel free to use and extend this package to suit your weather-related needs. If you encounter any issues, please refer to the WeatherAPIException and WeatherServiceException classes for error handling.