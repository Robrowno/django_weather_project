import datetime
import requests
from django.shortcuts import render


def home(request):
    """Render home.html template"""

    # Get API key from openweathermap.org
    API_KEY = open("API_KEY", "r").read().strip()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
    forecast_weather_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid={}&exclude=current,minutely,hourly,alerts"

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecast1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_weather_url)
        if city2:
            weather_data2, daily_forecast2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_weather_url)
        else:
            weather_data2, daily_forecast2 = None, None
        
        context = {
            'weather_data1': weather_data1,
            'daily_forecast1': daily_forecast1,
            'weather_data2': weather_data2,
            'daily_forecast2': daily_forecast2,
        }
        return render(request, 'weatherApp/home.html', context)
    else:
        return render(request, 'weatherApp/home.html')
    
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_weather_url):
    current_weather_response = requests.get(current_weather_url.format(city, api_key))
    current_weather_response.raise_for_status()
    current_weather = current_weather_response.json()

    forecast_response = requests.get(forecast_weather_url.format(current_weather['coord']['lat'], current_weather['coord']['lon'], api_key))
    forecast_response.raise_for_status()
    forecast_weather = forecast_response.json()

    weather_data = {
        'city': city,
        'temperature': round(current_weather['main']['temp'], 2),
        'description': current_weather['weather'][0]['description'],
        'icon': current_weather['weather'][0]['icon'],
        'humidity': current_weather['main']['humidity'],
        'wind_speed': current_weather['wind']['speed'],
        'pressure': current_weather['main']['pressure'],
        'sunrise': datetime.datetime.fromtimestamp(current_weather['sys']['sunrise']).strftime('%H:%M:%S'),
        'sunset': datetime.datetime.fromtimestamp(current_weather['sys']['sunset']).strftime('%H:%M:%S'),
    }

    daily_forecast = []
    for data in forecast_weather['daily'][:5]:
        daily_forecast.append({
            'date': datetime.datetime.fromtimestamp(data['dt']).strftime('%d-%m-%Y'),
            'temperature': round(data['temp']['day'], 2),
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'humidity': data['humidity'],
            'wind_speed': data['wind_speed'],
            'pressure': data['pressure'],
        })

    return weather_data, daily_forecast
