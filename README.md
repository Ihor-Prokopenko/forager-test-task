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
- `request_current_weather(self, city_name: str)`: Request the current weather for a specific city.
- `request_forecast(self, city_name: str)`: Request the forecast for a specific city.


## Example using WeatherAPIClient:
```python
from weather_client import WeatherAPIClient

# >>>> Retrieve and set your api key <<<<
api_key = "your_weather_api_key"

# >>>> create an instance of the CLIENT <<<<
client = WeatherAPIClient(api_key)

# >>>> request weather by city name via CLIENT <<<
weather_in_london = client.request_current_weather('London')
print(weather_in_london)
# City: London, Temp: 4.0, Condition: Partly cloudy, Last Updated: 2024-01-07 17:15
print(weather_in_london.condition)
# Partly cloudy
print(weather_in_london.temperature)
# 4.0

# >>>> request weather forecast by city name via CLIENT <<<<
forecast_for_london = client.request_forecast('London')
print(forecast_for_london)
# City: London, Avg_temp: 3.5, Condition: Patchy rain possible, Date: 2024-01-07
print(forecast_for_london.avg_temp)
# 3.5
print(forecast_for_london.date)
# 2024-01-07
print(forecast_for_london.condition)
# Patchy rain possible
```

***

## WeatherService Class

The WeatherService class manages weather-related operations and results. Retrieve current weather or specified one or multiple cities as well.

Attributes:

- `_results (list[WeatherResult])`: A list of WeatherResult objects.
- `_api_client (WeatherAPIClient)`: An instance of the WeatherAPIClient class.

Public methods:

 - `request_current_weather(self, city_name: str | list[str])`: Gets and saves the current weather for one or multiple cities.
 - `request_forecast(self, city_name: str | list[str])`: Gets and saves the forecast for one or multiple cities.
 - `save_weather(self, weather_obj: WeatherResult | list[WeatherResult])`: Saves weather results in the WeatherService.
 - `save_forecasts(self, forecast_obj: ForecastResult | list[ForecastResult])`: Saves forecast results in the WeatherService.
 - `get_weather(self, city_name: str | list[str])`: Gets weather results for a specific city or all cities.
 - `get_forecast(self, city_name: str | list[str])`: Gets forecast results for a specific city or all cities.
 - `clear_weather(self, city_name: str | list[str])`: Clears weather results for a specific city or all cities.
 - `clear_forecast(self, city_name: str | list[str])`: Clears forecast results for a specific city or all cities.


## Example using WeatherService:
```python
from weather_client import WeatherAPIClient, WeatherService

api_key = "your_weather_api_key"

# >>>> create an instance of the CLIENT <<<<
client = WeatherAPIClient(api_key)

# >>>> create an instance of the SERVICE <<<<
service = WeatherService(client)

# >>> get weather and forecast via CLIENT <<<<
weather_in_london = client.request_current_weather('London')
forecast_for_london = client.request_forecast('London')

# >>>> save the results via SERVICE <<<<
saved_forecast = service.save_forecasts(forecast_for_london)
saved_weather = service.save_weather(weather_in_london)
print(saved_forecast)
# City: London, Avg_temp: 3.5, Condition: Patchy rain possible, Date: 2024-01-07
print(saved_weather)
# City: London, Temp: 4.0, Condition: Partly cloudy, Last Updated: 2024-01-07 17:00


# >>>> request and save weather and forecast by city name via SERVICE <<<<
cities = ['London', 'Paris']
service.request_forecast(cities)
service.request_current_weather(cities)

print(service.get_forecasts())
# [object.ForecastResult(city_name=London, date=2024-01-07), object.ForecastResult(city_name=Paris, date=2024-01-07)]
print(service.get_weather())
# [object.WeatherResult(city_name=London), object.WeatherResult(city_name=Paris)]


# >>>> get the count of stored results <<<<
print(service.get_weather_count())
# 2
print(service.get_forecasts_count())
# 2


# >>>> get the results as a string <<<<
print(service.get_weather_as_str())
# City: London, Temp: 4.0, Condition: Partly cloudy, Last Updated: 2024-01-07 17:15
# City: Paris, Temp: 3.0, Condition: Overcast, Last Updated: 2024-01-07 18:15
print(service.get_forecasts_as_str())
# City: London, Avg_temp: 3.5, Condition: Patchy rain possible, Date: 2024-01-07
# City: Paris, Avg_temp: 4.1, Condition: Patchy rain possible, Date: 2024-01-07


# >>>> deletion results for specific or all cities <<<<
success = service.clear_forecasts('London')
print(success)
# True
print(service.get_forecasts())
# [object.ForecastResult(city_name=Paris, date=2024-01-07)]

service.clear_weather()
print(service.get_weather())
# []
```

***

***

## Conclusion
Feel free to use and extend this package to suit your weather-related needs. If you encounter any issues, please refer to the WeatherAPIException and WeatherServiceException classes for error handling.