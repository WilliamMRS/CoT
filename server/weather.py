import json
from metno_locationforecast import Place, Forecast

def get_forecast():
    USER_AGENT = "metno-locationforecast/1.0 jenstho@stud.ntnu.no"
    Trondheim = Place("Trondheim", 63.42024, 10.40122)
    Trondheim_forecast = Forecast(Trondheim, USER_AGENT)
    Trondheim_forecast.update()
    return(Trondheim_forecast)
print(get_forecast())

def liveForecast():
    forecast = Future_forecast()
    First_interval = forecast.data.intervals[2]
    return First_interval

def temperature():
    data = str(Get_data_now().variables["air_temperature"]).split()[1].split("c")[0]
    return float(data)
#print(getTemperature())

def airPressure():
    pressure_data = Future_forecast().variables["air_pressure_at_sea_level"]
    return pressure_data
#print(get_air_pressure())