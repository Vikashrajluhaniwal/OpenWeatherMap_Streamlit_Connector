#!/usr/bin/env python
# coding: utf-8

# In[2]:


from streamlit.connections import ExperimentalBaseConnection
import requests, json
import datetime as dt
import streamlit as st
import pandas as pd
import math


# In[ ]:


class OpenWeatherMapConnection(ExperimentalBaseConnection):
    
    def _connect(self, **kwargs):
        """
        Establishes a new OpenWeatherMap connection.
        """
        
        kw = kwargs.copy()
        if 'api_key' in kw and len(kw['api_key'])>0:
            self._api_key = kw['api_key']
        else:
            self._api_key = st.secrets["api_key"]
    
    def cursor(self):
        """
        Returns OpenWeatherMap API key.

        Returns:
            api_key: OpenWeatherMap API key
        """
        
        return self._api_key
    
    def fetch(self, city_name, ttl=None, **kwargs):
        """
        Fetches the weather details for a particular city input from the OpenWeatherMap API.

        Args:
            city_name (string): A city name for which weather details are to be fetched.
            ttl (int) : Time to live
            

        Returns:
            pd.DataFrame: A Pandas Dataframe containing weather details like temperature, humidity, wind speed, sunrise & sunset time etc. for each city passed.
        """
        @st.cache_data(ttl=ttl)
        def _fetch(city_name: str, **kwargs):
            weather_details = {}
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + self._api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                weather_details['Temperature 🌡️'] = round(y["temp"]-273.15)
                weather_details['Feels Like'] = round(y["feels_like"]-273.15)
                weather_details['Humidity'] = str(y["humidity"]) + " %"
                weather_details['Wind Speed 🎈'] = str(math.ceil(x["wind"]["speed"]*3.6)) + " Km/h"
                weather_details['Description'] = x['weather'][0]['description']
                weather_details['Sunrise Time 🌅'] = dt.datetime.utcfromtimestamp(x['sys']['sunrise'] + x['timezone'])
                weather_details['Sunset Time 🌄'] = dt.datetime.utcfromtimestamp(x['sys']['sunset'] + x['timezone'])
            else:
                print(" City Not Found ")   
            return pd.DataFrame(weather_details, index = [0])
        return _fetch(city_name, **kwargs)

