""" FUNCTIONS MODULE - Auxiliar functions for the bot """

# Imports
import json
import requests
import logging
from geopy.geocoders import Nominatim



# Return data from openWeather API
def openWeatherAPI_call(lat, lon):
    # Call api
    openWeatherAPI = json.load(open("../data/tokens.json", "r"))["openWeather"]
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={openWeatherAPI}'
    re = requests.get(url)
    # Log status exception
    logging.error(re.raise_for_status())
    # Get results
    data = json.loads(re.text)
    # return weather data, temperature data, location
    return dict(data.get('weather')[0]), dict(data.get('main')), data["name"]


# Return city based on latitude and longitude
def getCity(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{lat}, {lon}")
    address = location.raw['address']
    return address.get('city', '')


# Return weather icon based on code
def getWeatherEmoji(weather_code):
    # Dictionary that relates weather Unicode emoji with weather condition codes from openWeatherAPI
    weather_emojis = {
        '\U000026A1': [210, 211, 212, 221],
        '\U000026C8': [200, 201, 202, 504, 531],
        '\U0001F329': [230, 231, 232],
        '\U0001F327': [300, 301, 302, 310, 311, 312, 313, 314, 321, 503, 504, 522],
        '\U0001F326': [500, 501, 520, 521],
        '\U0001F328': [511, 611, 612, 613, 615, 616],
        '\U00002744': [600, 601, 602, 620, 621, 622],
        '\U0001F32A': [771, 781],
        '\U0001F32B': [701, 721, 731, 741],
        '\U00002600': [800],
        '\U00002601': [801, 802, 803, 804]
    }
    return [k for k, v in weather_emojis.items() if weather_code in v][0]
