# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:57:36 2021

@author: Jensn
"""
from metno_locationforecast import Place, Forecast

def get_data_now():
    USER_AGENT = "metno_locationforecast/1.0 jenstho@stud.ntnu.no"
    Trondheim = Place("Trondheim", 63.42024, 10.40122)
    Trondheim_forecast = Forecast(Trondheim, USER_AGENT)
    Trondheim_forecast.update()
   # First_interval = Trondheim_forecast.data.intervals[2]
    return(Trondheim_forecast)
    
#print( get_data_now())


def getTemperature():
    data = get_data_now().variables["air_temperature"]
    return data

#print(getTemperature())

def get_Cloud_area_fraction():
    Cloud_data = get_data_now().variables["cloud_area_fraction"]
    return Cloud_data
#print(get_Cloud_area_fraction())

def get_air_pressure():
    pressure_data = get_data_now().variables["air_pressure_at_sea_level"]
    return pressure_data
#print(get_air_pressure())

def future_forecast():
    future_forecast = get_data_now()
    First_interval = future_forecast.data.intervals[2]
    
    return First_interval
    
    

print(future_forecast())
    
    

    
    



