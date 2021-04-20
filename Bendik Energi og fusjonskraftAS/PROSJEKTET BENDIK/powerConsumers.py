from entsoe import EntsoeRawClient
from datetime import date, datetime
import requests
import json
import pandas as pd
import key as key #Personlige tokens


token = key.token # Henter CoT Token fra key.py fil
api_key = key.api_key # Token til ENTSOE fra key.py

# Definerer "kontaktinfo" til apparatene i CoT
info_stove = {'Key':'17673','Value':0,'Token':token} 
info_dishwasher = {'Key':'0','Value':0,'Token':token} 
info_coffeeMachine = {'Key':'0','Value':0,'Token':token} 
info_fridge = {'Key':'0','Value':0,'Token':token} 
info_shower = {'Key':'0','Value':0,'Token':token} 
info_clothesWasher = {'Key':'0','Value':0,'Token':token} 



def powerPriceFetch(api_key) : # Funksjon for å hente inn strømpriser fra Entsoe
    client = EntsoeRawClient(api_key)
    start = pd.Timestamp('20210413', tz="Europe/Oslo")
    end = pd.Timestamp('20210414', tz="Europe/Oslo")
    country_code = 'NO_3'  # Norway, Trodelag
    data = client.query_day_ahead_prices(country_code, start, end)
    print(data)
    return data # SPESIFISERE HVILKEN DATA SOM SKAL RETURNERES???

# powerPriceFetch(api_key)

def status(unitState): # funksjon for å sjekke tilstand
    if unitState() == 1:
        return True
    else:
        return False


def powerConsumptionLogging(unit): #Funksjon for å legge forbruket fra de ulike apparatene til i en fil
    consumption = unit
    with open("powerUsage.csv", "w") as f:
        f.write(consumption)


def putCoT(data, status) : #Tar inn info_apparat og oppdaterer status i CoT 
    data["Value"] = status
    if (data["Value"] > 1 ) : # ErrorHandling
        print("value to high")
    else :
        requests.put("https://circusofthings.com/WriteValue",data=json.dumps(data),headers={'Content-Type':'application/json'})


class powerConsumer: #De apparatene i leiligheten som må kjøres. eks komfyr og oppvaskmaskin
    def __init__(self, room, effect, numOfUses, payload ) :#Rom, forbruk i watt, antall bruk før kjøring, status for av/på
        self.room = room
        self.effect = effect
        self.numOfUses = numOfUses
        self.payload = payload

    def powerOn(self):
        totalUses = 0
        if self.status == True:
            totalUses +1
        if totalUses == self.numOfUses:
            return self.effect
    def status(self) :
        response = requests.get("https://circusofthings.com/ReadValue", params = self.payload)
        return json.loads(response.content)["Value"]

    def printShit(self):
        print(self.room)
        print(self.effect)
        print(self.numOfUses)
        print(self.status)

    

# Definere de ulike strømforbrukennde apparatene
# Velge hvem som er aktive, og hvem som er av
# legges i en liste for totalt strømforbruk  
# Vis forburk i realtid og historisk i graf
# Ta inn sanntidsvaluta for EUR til NOK
# Vis kostand i graf (realtid og historisk)



consumers = {
# Definerer ulike strømforbrukende apparater 
"stove" : powerConsumer("kitchen", 2200, 5, info_stove),
"dishwasher" : powerConsumer("kitchen",2000, 5, info_dishwasher),
"coffeeMachine" : powerConsumer("kitchen", 1500, 1, info_coffeeMachine),
"fridge" : powerConsumer("kitchen", 160, 1, info_fridge),
"clothesWasher" : powerConsumer("bathroom", 2500, 1, info_clothesWasher),
"shower" : powerConsumer("bathroom", 1000, 1, info_shower),
}

#list(stove, dishwasher, coffeeMachine, fridge, clothesWasher, shower)
#print (consumers["stove"].status(info_stove))
print (consumers["stove"].status())

def updateConsumerStatus(dictionary):
    for i in dictionary:
        dictionary[i].status()
        print (dictionary[i].status())

updateConsumerStatus(consumers)




