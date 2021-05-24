from django.shortcuts import render
import pandas as pd
import requests


def index(request):
    df = pd.read_csv('worldcities.csv')

    if 'city' in request.GET:
        city = request.GET['city']
        city = city.title()
        if df[df['city_ascii'] == city]['city_ascii'].any():
            lat = df[df['city_ascii'] == city]['lat']
            lon = df[df['city_ascii'] == city]['lng']
            url = "https://climacell-microweather-v1.p.rapidapi.com/weather/realtime"
            querystring = {"unit_system": "si",
                           "fields": ["precipitation", "precipitation_type", "temp", "cloud_cover", "wind_speed",
                                      "weather_code"], "lat": lat, "lon": lon
                           }
            headers = {'x-rapidapi-host': "climacell-microweather-v1.p.rapidapi.com",
                       'x-rapidapi-key': "a1ca7cac7bmsh7481cbdd1b05541p170fb7jsnfb74af885ed7"
                       }
            response = requests.request("GET", url, headers=headers, params=querystring).json()

            context = {'city_name': city, 'temp': response['temp']['value'],
                       'weather_code': response['weather_code']['value'],
                       'wind_speed': response['wind_speed']['value'],
                       'precipitation_type': response['precipitation_type']['value']
                       }
        else:
            context = {'none': 'no data try later'}
    else:
        context = {'none': 'no data try later'}
    return render(request, 'index.html', context)