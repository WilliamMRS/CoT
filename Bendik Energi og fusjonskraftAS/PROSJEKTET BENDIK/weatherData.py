# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:57:36 2021
@author: Jensn
"""
import json
from metno_locationforecast import Place, Forecast

def Future_forecast():
    USER_AGENT = "metno_locationforecast/1.0 jenstho@stud.ntnu.no"
    Trondheim = Place("Trondheim", 63.42024, 10.40122)
    Trondheim_forecast = Forecast(Trondheim, USER_AGENT)
    Trondheim_forecast.update()
    return(Trondheim_forecast)
print(Future_forecast())

def getTemperature():
    data = Future_forecast().variables["air_temperature"]
    return data
#print(getTemperature())

def get_Cloud_area_fraction():
    Cloud_data = Future_forecast().variables["cloud_area_fraction"]
    return Cloud_data
#print(get_Cloud_area_fraction())

def get_air_pressure():
    pressure_data = Future_forecast().variables["air_pressure_at_sea_level"]
    return pressure_data
#print(get_air_pressure())

def Get_data_now():
    forecast = Future_forecast()
    First_interval = forecast.data.intervals[2]
    return First_interval


