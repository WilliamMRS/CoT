import json
from metno_locationforecast import Place, Forecast

def forecast():
    USER_AGENT = "metno-locationforecast/1.0 jenstho@stud.ntnu.no"
    Trondheim = Place("Trondheim", 63.42024, 10.40122)
    Trondheim_forecast = Forecast(Trondheim, USER_AGENT)
    Trondheim_forecast.update()
    return(Trondheim_forecast)


def liveForecast():
    forecastData = forecast()
    First_interval = forecastData.data.intervals[2]
    return First_interval

def temperature():
    data = str(liveForecast().variables["air_temperature"]).split()[1].split("c")[0]
    return float(data)

#print(temperature())

""" def airPressure():
    pressure_data = forecast().variables["air_pressure_at_sea_level"]
    return pressure_data
print(airPressure()) """