from django.shortcuts import render
from django.conf import settings
import http.client
from urllib.parse import quote_plus
from datetime import date
from django.contrib import messages
import json


def index(request):
    """A view that renders index page"""

    weather = fetchWeather(request)

    context = {
        "weather": weather,
    }

    return render(request, 'home/home.html', context)


def fetchWeather(request):
    """ Fetches weather and stores it in current session. To keep api calls to an minimum
        Only one call per day and session. """

    weather = request.session.get('weather', {})
    today = date.today()

    if 'dt' in weather:
        print(today, date.fromtimestamp(weather['dt']))
        if date.fromtimestamp(weather['dt']) == today:
            return weather

    try:
        conn = http.client.HTTPSConnection(
            "api.openweathermap.org")

        conn.request(
            "GET", f"/data/2.5/weather?q=nowhere&units=metric&appid={settings.WEATHER_API_KEY}")

        res = conn.getresponse()
        data = res.read()
        weather = json.loads(data)
        request.session['weather'] = weather
    except:
        messages.error(request, 'Failed to fetch weather data.')

    return weather
