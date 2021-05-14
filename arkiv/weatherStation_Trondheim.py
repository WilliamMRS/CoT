# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:57:36 2021

@author: Jensn
"""
from metno_locationforecast import Place, Forecast

def Future_forecast():
    USER_AGENT = "metno_locationforecast/1.0 jenstho@stud.ntnu.no"
    Trondheim = Place("Trondheim", 63.42024, 10.40122)
    Trondheim_forecast = Forecast(Trondheim, USER_AGENT)
    Trondheim_forecast.update()
    return(Trondheim_forecast)


def Get_data_now():
    get_data_now = Future_forecast()
    First_interval = get_data_now.data.intervals[2]
    
    return First_interval   
print(Get_data_now())

def getTemperature():
    data = Get_data_now().variables["air_temperature"]
    return data

#print(getTemperature())

def get_Cloud_area_fraction():
    Cloud_data = Get_data_now().variables["cloud_area_fraction"]
    return Cloud_data
print(get_Cloud_area_fraction())

def get_air_pressure():
    pressure_data = Get_data_now().variables["air_pressure_at_sea_level"]
    return pressure_data
#print(get_air_pressure())





def SolarEnergy():
    a= (200000/(365*24)) #Norge = 200k - H
    b= 150 # kvm - A
    c= (19.7/100) # effektfaktor - R
    d= 1 # - PR
    
    Cloudcover = 0
    LimitCloud = 0.8
    
    if get_Cloud_area_fraction() > LimitCloud:
        Cloudcover =0.8
        #print("test1")
    elif get_Cloud_area_fraction() < LimitCloud:
        Cloudcover = get_Cloud_area_fraction()
        print(type(get_Cloud_area_fraction()))
    e= (a*b*c*(d - Cloudcover))
    
     
    return (e/1000)
print(SolarEnergy())
        
    

    
    

    
    



