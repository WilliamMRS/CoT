import requests
import json

def fetchCurrency() : # Henter oppdatert valuttakurs
    response = requests.get("https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=1&locale=no")
    # Endre på lastNObservations= for å få flere tidsenheter med kurser
    return json.loads(response.content)["data"]["dataSets"][0]["series"]["0:0:0:0"]["observations"]["0"][0]

print(fetchCurrency())