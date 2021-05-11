from entsoe import EntsoeRawClient
import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
import key as key
import datetime

api_key = key.api_key # Token til ENTSOE fra key.py

# def fetchCurrencyDynamic() : # Henter oppdatert valuttakurs

""" def fetchCurrency() : # Henter oppdatert valuttakurs
    response = requests.get("https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=1&locale=no")
    #Endre på lastNObservations= for å få flere tidsenheter med kurser
    return json.loads(response.content)["data"]["dataSets"][0]["series"]["0:0:0:0"]["observations"]["0"][0] """




def fetchCurrency(startPeriod, endPeriod) : # Y/M/D
    payload = {"startPeriod" : startPeriod, "endPeriod" : endPeriod, "locale" : "no"}
    response = requests.get("https://data.norges-bank.no/api/data/EXR/B.GBP.NOK.SP?format=sdmx-json&", data = json.dumps(payload))
    return json.loads(response.content)["data"]["dataSets"][0]["series"]["0:0:0:0"]["observations"]["0"][0]

def powerPriceFetch(api_key) : # Funksjon for å hente inn strømpriser fra Entsoe
    client = EntsoeRawClient(api_key)
    start = pd.Timestamp('20210413', tz="Europe/Oslo")
    end = pd.Timestamp('20210414', tz="Europe/Oslo")
    country_code = 'NO_3'  # Norway, Trondelag
    response = client.query_day_ahead_prices(country_code, start, end)
    return response # SPESIFISERE HVILKEN DATA SOM SKAL RETURNERES???

def powerPriceFetch2(api_key, start, end) : 
    url = "https://transparency.entsoe.eu/api"
    documentType = "A44" # specifying we want the price document
    processType = "A01" #specifying we want Day Ahead
    zone = "NO_3" # Code for Norway 
    startPeriod = start
    endPeriod = end
    token = api_key
    payload = {"securityToken" : token, "documentType" : documentType, "processType" : processType,
    "in_domain" : zone, "out_domain" : zone, "periodStart" : startPeriod, "periodEnd" : endPeriod}
    #response = requests.get("https://transparency.entsoe.eu/api", data = json.dumps(payload))
    response = requests.get("https://transparency.entsoe.eu/api?securityToken=fa3385eb-bcee-4913-8673-824d6e8b9dd0&documentType=A65&processType=A01&outBiddingZone_Domain=10YNO-0--------C&periodStart=202104012300&periodEnd=202104022300")
    return (response.content)

#https://transparency.entsoe.eu/api?securityToken=fa3385eb-bcee-4913-8673-824d6e8b9dd0&documentType=A65&processType=A01&outBiddingZone_Domain=10YNO-0--------C&periodStart=202104012300&periodEnd=202104022300
https://transparency.entsoe.eu/api?securityToken=fa3385eb-bcee-4913-8673-824d6e8b9dd0&documentType=A44&in_Domain=10YNO-0--------C&out_domain=10YNO-0--------C&periodStart=201512312300&periodEnd=201612312300
https://transparency.entsoe.eu/api?securityToken=fa3385eb-bcee-4913-8673-824d6e8b9dd0&documentType=A44&in_Domain=10YCZ-CEPS-----N&out_Domain=10YCZ-CEPS-----N&periodStart=201512312300&periodEnd=201612312300



#def xmlParser():

periodStart = "20210401"
periodEnd = "20210402"

print(powerPriceFetch2(api_key, periodStart, periodEnd))


def powerPriceNok(periodStart, periodEnd, api_key) : 
    rate = fetchCurrency(periodStart, periodEnd)
    price = powerPriceFetch(api_key)
    return (rate * price) 

#print(powerPriceNok(periodStart, periodEnd, api_key))


