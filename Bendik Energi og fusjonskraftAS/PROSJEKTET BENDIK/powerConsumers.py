from entsoe import EntsoeRawClient
import time 
import requests
import json
import pandas as pd
import csv
import key as key #Personlige tokens


token = key.token # Henter CoT Token fra key.py fil
api_key = key.api_key # Token til ENTSOE fra key.py


# todo 
# Dele opp rommene sitt strømforbruk 


def powerPriceFetch(api_key) : # Funksjon for å hente inn strømpriser fra Entsoe
    client = EntsoeRawClient(api_key)
    start = pd.Timestamp('20210413', tz="Europe/Oslo")
    end = pd.Timestamp('20210414', tz="Europe/Oslo")
    country_code = 'NO_3'  # Norway, Trondelag
    response = client.query_day_ahead_prices(country_code, start, end)
    return responce # SPESIFISERE HVILKEN DATA SOM SKAL RETURNERES???

print (powerPriceFetch(api_key))

def putCoT(data, status) : #Tar inn info_apparat og oppdaterer med ny status i CoT 
    data["Value"] = status
    if (data["Value"] > 1 ) : # ErrorHandling
        print("value to high")
    else :
        requests.put("https://circusofthings.com/WriteValue",data=json.dumps(data),headers={'Content-Type':'application/json'})


class powerConsumer: # Klassen til alle strømforbrukennde apparater i leiligheten. 
    def __init__(self, room, effect, numOfUses, payload ) :# Rom, forbruk i watt, antall bruk før kjøring, kommunikasjonsnøkkel
        self.room = room
        self.effect = effect
        self.numOfUses = numOfUses
        self.payload = payload

    def powerOn(self): #Sjekker hvor mange ganger apparatet er blitt brukt
        totalUses = 0
        if self.status == True:
            totalUses +1
        if totalUses == self.numOfUses:
            return self.effect

    def status(self) : # Henter AV/PÅ status fra CoT
        response = requests.get("https://circusofthings.com/ReadValue", params = self.payload)
        return json.loads(response.content)["Value"]

    def changeEffect(self) :
        response = 1#PLACEHOLDER
        return response 


    def printShit(self): #PrintShit
        print(self.room)
        print(self.effect)
        print(self.numOfUses)
        print(self.status)

# Ta inn sanntidsvaluta for EUR til NOK   
# Vis forburk i realtid og historisk i graf
# Vis kostand i graf (realtid og historisk)


# Definerer "kontaktinfo" til apparatene i CoT
info_stove = {'Key':'17673','Value':0,'Token':token} 
info_dishwasher = {'Key':'17673','Value':0,'Token':token} 
info_coffeeMachine = {'Key':'17673','Value':0,'Token':token} 
info_fridge = {'Key':'17673','Value':0,'Token':token} 
info_shower = {'Key':'17673','Value':0,'Token':token} 
info_washingMachine = {'Key':'17673','Value':0,'Token':token} 
info_shower = {'Key':'17673','Value':0,'Token':token}
info_heatingCable = {'Key':'17673','Value':0,'Token':token}
info_light_1 = {'Key':'17673','Value':0,'Token':token}
info_curtains_1 = {'Key':'17673','Value':0,'Token':token}
info_heater_1 = {'Key':'17673','Value':0,'Token':token}
info_light_2 = {'Key':'17673','Value':0,'Token':token}
info_curtains_2 = {'Key':'17673','Value':0,'Token':token}
info_heater_2 = {'Key':'17673','Value':0,'Token':token}
info_light_3 = {'Key':'17673','Value':0,'Token':token}
info_curtains_3 = {'Key':'17673','Value':0,'Token':token}
info_heater_3 = {'Key':'17673','Value':0,'Token':token}
info_light_4 = {'Key':'17673','Value':0,'Token':token}
info_curtains_4 = {'Key':'17673','Value':0,'Token':token}
info_heater_4 = {'Key':'17673','Value':0,'Token':token}

consumers = { # Definerer ulike strømforbrukende apparater 
#Legg inn nye objekter her
"stove" : powerConsumer("kitchen", 2200, 1, info_stove),
"dishwasher" : powerConsumer("kitchen",2000, 4, info_dishwasher),
"coffeeMachine" : powerConsumer("kitchen", 1500, 1, info_coffeeMachine),
"fridge" : powerConsumer("kitchen", 160, 1, info_fridge),
"washingMachine" : powerConsumer("bathroom", 2500, 4, info_washingMachine),
"shower" : powerConsumer("bathroom", 1000, 1, info_shower),
"heatingCable" : powerConsumer("bathroom", 1000, 1, info_heatingCable),
"light_1" : powerConsumer("bedroom_1", 40, 1, info_light_1),
"curtains_1" : powerConsumer("bedroom_1", 40, 1, info_curtains_1),
"heater_1" : powerConsumer("bedroom_1", 40, 1, info_heater_1),
"light_2" : powerConsumer("bedroom_2", 40, 1, info_light_2),
"curtains_2" : powerConsumer("bedroom_2", 40, 1, info_curtains_2),
"heater_2" : powerConsumer("bedroom_2", 40, 1, info_heater_2),
"light_3" : powerConsumer("bedroom_3", 40, 1, info_light_3),
"curtains_3" : powerConsumer("bedroom_3", 40, 1, info_curtains_3),
"heater_3" : powerConsumer("bedroom_3", 40, 1, info_heater_3),
"light_4" : powerConsumer("bedroom_4", 40, 1, info_light_4),
"curtains_4" : powerConsumer("bedroom_4", 40, 1, info_curtains_4),
"heater_4" : powerConsumer("bedroom_4", 40, 1, info_heater_4),
}

rooms = {
"Total" : consumers,
"kitchen" : [],
"bathroom" : [],
"bedroom_1" : [],
"bedroom_2" : [],
"bedroom_3" : [],
"bedroom_4" : [],
}
def putObjectsInRooms(consumerList, roomList) :
    for key in roomList.keys() :
        for i in consumerList :
            if consumerList[i].room == key :
                roomList[key].append(consumerList[i])

""" print (consumers["stove"].status()) """

def updateConsumerStatus(dictionary): # Oppdaterer de ulike objektene sin powerStatus (Av/PÅ) fra CoT
    for i in dictionary:
        dictionary[i].status()

def powerConsumptionLogging(unit): #Funksjon for å skrive til en .csv fil
    kW = unit/1000 # Gjør om til kiloWatt
    now = time.strftime('%d-%m-%Y %H:%M:%S')
    print("The time is" + now)
    with open("powerUsage.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, str(kW)])

# status(consumers, "dishwasher")
# powerConsumptionLogging(consumers["dishwasher"])
#print (consumers["stove"].status(info_stove))

def logThis(dictionary) : # Oppdaterer status på apparater og skriver forbruket til csv.fil. Tar inn dictionary med apparat objektene
    updateConsumerStatus(dictionary)
    currentConsumption = 0
    for i in dictionary :
        if dictionary[i].status() == 1 :
            currentConsumption += dictionary[i].effect
        else : 
            pass
    print ("The current consumptionn is " + str(currentConsumption))
    powerConsumptionLogging(currentConsumption)   

# placeholderTitle(consumers)

putObjectsInRooms(consumers, rooms)







""" # Transform your dictionary to pandas dataframe
df = pd.DataFrame.from_records([data2], index=[0])

# Insert timestamp at first column (as desired)
df.insert(0, 'timestamp', time.strftime('%d-%m-%Y %H:%M:%S'))

# Write to csv
df.to_csv('my_file.csv', index=False) """


""" 
Dusj:fastverdi (kWh)> 
Varmekabler på baderom: én kWh-verdi for normal bruk, én for natt-/dagsenking.> 
Stekeplater og stekeovn: forenkles til én kWh-verdi for hver, uansetttype bruk.> 
Panelovner på soverommene: sett opp en enkel modell for kWh-forbruketavhengig av hva termostaten er satt til, 
samt utetemperatur og vindstyrke. Kanskje også sol og 
skydekke, for gruppene som ønsker enekstra utfordring.RPien henter inn værdata.> 
Vaskemaskinen: anta at den kjøres Xganger i uka, og forbrukerYkWh. Videre at hver kjøring avvaskemaskinen følges av kjøring av tørketrommelensomforbrukerZkWh> TVen i TV-stua: anta at dener slått på med et forbruk på XkWhså lenge TV-stua er booket.> 
Oppvaskmaskinen:Én frokost fyller 10%, én lunsj 15%og én middag 25%. Forbruket er XkWh for hver kjøring. Denkjører når fyllingsgraden er>90%og < 100%-Modellereproduksjonen:>
Solcellepanelet:produksjonenavhenger av solcelletypen (plukk et konkret panel og sjekk databladet), virkningsgraden, solens posisjon, skydekke, lufttemperatur,etc.RPienhenter inn værdata.
"""