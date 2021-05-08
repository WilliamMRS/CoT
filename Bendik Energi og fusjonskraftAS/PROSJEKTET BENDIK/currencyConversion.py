from entsoe import EntsoeRawClient
import requests
import json
import pandas as pd
import key as key
import datetime

api_key = key.api_key # Token til ENTSOE fra key.py

def fetchCurrencyDynamic() : # Henter oppdatert valuttakurs
    response = requests.get("https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=1&locale=no")
    #Endre på lastNObservations= for å få flere tidsenheter med kurser
    return json.loads(response.content)["data"]["dataSets"][0]["series"]["0:0:0:0"]["observations"]["0"][0]

def fetchCurrency(startPeriod, endPeriod) : # Y/M/D
    payload = {"startPeriod" : startPeriod, "endPeriod" : endPeriod, "locale" : "no"}
    response = requests.get("https://data.norges-bank.no/api/data/EXR/B.GBP.NOK.SP?format=sdmx-json&", data = json.dumps(payload)) #startPeriod=2020-05-03&endPeriod=2021-05-03&locale=no")
    return json.loads(response.content)["data"]["dataSets"][0]["series"]["0:0:0:0"]["observations"]["0"][0]

def powerPriceFetch(api_key) : # Funksjon for å hente inn strømpriser fra Entsoe
    client = EntsoeRawClient(api_key)
    start = pd.Timestamp('20210413', tz="Europe/Oslo")
    end = pd.Timestamp('20210414', tz="Europe/Oslo")
    country_code = 'NO_3'  # Norway, Trondelag
    response = client.query_day_ahead_prices(country_code, start, end)
    return response # SPESIFISERE HVILKEN DATA SOM SKAL RETURNERES???


periodStart = "20210401"
periodEnd = "20210402"

print(powerPriceFetch(api_key))

def powerPriceNok(periodStart, periodEnd, api_key) : 
    rate = fetchCurrency(periodStart, periodEnd)
    price = powerPriceFetch(api_key)
    return (rate * price) 

#print(powerPriceNok(periodStart, periodEnd, api_key))


