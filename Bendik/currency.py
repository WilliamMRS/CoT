from entsoe import EntsoePandasClient
import requests
import json
import pandas as pd
import key as key
import datetime

api_key = key.api_key # Token til ENTSOE fra key.py

# def fetchCurrencyDynamic() : # Henter oppdatert valuttakurs

def fetchCurrency(startPeriod, endPeriod) : # Y/M/D
    """ 
    Henter valuttakurs fra Norges bank. 
    """
    payload = {"startPeriod" : str(startPeriod), "endPeriod" : str(endPeriod), "locale" : "no"}
    response = requests.get("https://data.norges-bank.no/api/data/EXR/B.GBP.NOK.SP?format=sdmx-json&", 
                                data = json.dumps(payload))
    return json.loads(response.content)["data"]["dataSets"][0]["series"]["0:0:0:0"]["observations"]["0"][0]

def powerPriceFetch(api_key, start, end) : 
    """ 
    Henter strømpris fra et gitt tidsrom fra ENTSO E sin strømprisdatabase.  
    I EUR/MWh
    """
    client = EntsoePandasClient(api_key)
    country_code = 'NO_3'  # Norway, Trondelag
    response = client.query_day_ahead_prices(country_code, start = start, end = end)
    return response[0]


startTime = "20210413"
endTime = "20210414"


def powerPriceInNok(start, end) : 
    startPD = pd.Timestamp(str(start), tz="Europe/Oslo")
    endPD = pd.Timestamp(str(end), tz="Europe/Oslo")
    rate = float(fetchCurrency(start, end))
    price = int(powerPriceFetch(key.api_key, startPD, endPD))
    return ((rate * price)/1000)  # NOK/KWh



