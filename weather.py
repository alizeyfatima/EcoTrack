import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):

    url = "https://api.openweathermap.org/data/2.5/weather"

    parameters = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=parameters)

    if response.status_code == 200:

        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        return temperature, humidity, description

    else:

        print("Unable to retrieve weather data.")
        print("Status code:", response.status_code)
        print("Error:", response.text)

        return None, None, None