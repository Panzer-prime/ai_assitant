import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import json
from src.plugin.base_plugin import BasePluging

class Weather(BasePluging):
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("WEATHER_KEY")
        self.limit = 5


    def get_cords_by_place(self, location):
        geocoding_url = "http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={api_key}".format(location=location,api_key= self.api_key)
        response = requests.get(geocoding_url)
        response_data = response.json()

        return (response_data[0]["lat"], response_data[0]["lon"])

    
    def get_weather(self, location):
        if not self.api_key:
            print("key is missing check path")
        
        lat, lon = self.get_cords_by_place(location)
        weather_url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric".format(lat = lat,lon= lon, api_key = self.api_key)

        response = requests.get(weather_url)
        response_data = response.json()

        print(response_data["main"]['temp'], response_data["main"]['feels_like'])
        
        return f"Weather in the required place: {location} is currently {response_data["main"]['temp']} celcius but feels like {response_data["main"]['feels_like']} "
    

    def run(self):
        self.get_weather()

    def can_run(self,value: str):
        return value == "weather"