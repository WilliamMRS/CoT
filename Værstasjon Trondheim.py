# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:57:36 2021

@author: Jensn
"""

from metno_locationforecast import Place, Forecast
import datetime as dt
import pandas as pd
def værdata():
    USER_AGENT = "metno_locationforecast/1.0 jenstho@stud.ntnu.no"
    
    Trondheim = Place("Trondheim", 63.42024, 10.40122)
    Trondheim_forecast = Forecast(Trondheim, USER_AGENT, "complete")
    Trondheim_forecast.update()
    print(Trondheim_forecast)
    
    First_interval = Trondheim_forecast.data.intervals[0]
    
    Trondheim_forecast.update()
    
    tomorrow= dt.date.today() + dt.timedelta()
   
    tomorrow_intervals = Trondheim_forecast.data.intervals_for(tomorrow)
    print("Forecast for tomorrow in Trondheim:\n")
    for interval in tomorrow_intervals:
        print(interval)
    
    
    
    print(First_interval)
    
    print(f"Duration: {First_interval.duration}")
    print()
    
    rain = First_interval.variables["precipitation_amount"]
    print(rain)
    
    print(f"Rain values: {rain.value}")
    print(f"Rain units: {rain.units}")
    
    print(First_interval.variables.keys())
    
    
    
værdata()

