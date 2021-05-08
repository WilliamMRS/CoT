import time 
import requests
import json
import pandas as pd
import csv
import key as key #Personlige tokens


token = key.token # Henter CoT Token fra key.py fil



# todo 
# Dele opp rommene sitt strømforbruk 

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
        response = 1 #PLACEHOLDER
        return response 

    def printShit(self): #PrintShit
        print(self.room)
        print(self.effect)
        print(self.numOfUses)
        print(self.status)


# Definerer "kontaktinfo" til apparatene i CoT
info_TV = {'Key':'24411','Value':0,'Token':token}
info_livingRoomLight = {'Key':'21989','Value':0,'Token':token}
info_stove = {'Key':'26299','Value':0,'Token':token} 
info_dishwasher = {'Key':'22562','Value':0,'Token':token} 
info_coffeeMachine = {'Key':'9242','Value':0,'Token':token} 
info_fridge = {'Key':'18863','Value':0,'Token':token}
info_kitchenHeater = {'Key':'3714','Value':0,'Token':token} 
info_kitchenLight = {'Key':'8485','Value':0,'Token':token} 
info_shower = {'Key':'29262','Value':0,'Token':token} 
info_washingMachine = {'Key':'28922','Value':0,'Token':token} 
info_heatingCable = {'Key':'373','Value':0,'Token':token}
info_light_1 = {'Key':'21462','Value':0,'Token':token}
info_curtains_1 = {'Key':'8365','Value':0,'Token':token}
info_heater_1 = {'Key':'20954','Value':0,'Token':token}
info_light_2 = {'Key':'5959','Value':0,'Token':token}
info_curtains_2 = {'Key':'8365','Value':0,'Token':token}
info_heater_2 = {'Key':'29644','Value':0,'Token':token}
info_light_3 = {'Key':'25206','Value':0,'Token':token}
info_curtains_3 = {'Key':'8365','Value':0,'Token':token}
info_heater_3 = {'Key':'3074','Value':0,'Token':token}
info_light_4 = {'Key':'10550','Value':0,'Token':token}
info_curtains_4 = {'Key':'8365','Value':0,'Token':token}
info_heater_4 = {'Key':'19494','Value':0,'Token':token}

consumers = { # Definerer ulike strømforbrukende apparater 
#Legg inn nye objekter her
"livingroomLight" : powerConsumer("livingroom", 40, 1, info_livingRoomLight),
"TV" : powerConsumer("livingroom", 0, 1, info_TV),
"stove" : powerConsumer("kitchen", 2200, 1, info_stove),
"dishwasher" : powerConsumer("kitchen",2000, 4, info_dishwasher),
"coffeeMachine" : powerConsumer("kitchen", 1500, 1, info_coffeeMachine),
"fridge" : powerConsumer("kitchen", 160, 1, info_fridge),
"kitchenHeater" : powerConsumer("kitchen", 0, 1, info_kitchenHeater),
"kitchenLight" : powerConsumer("kitchen", 40, 1, info_kitchenLight),
"washingMachine" : powerConsumer("bathroom", 2500, 4, info_washingMachine),
"shower" : powerConsumer("bathroom", 1000, 1, info_shower),
"heatingCable" : powerConsumer("bathroom", 1000, 1, info_heatingCable),
"light_1" : powerConsumer("bedroom_1", 40, 1, info_light_1),
"curtains_1" : powerConsumer("bedroom_1", 0, 1, info_curtains_1),
"heater_1" : powerConsumer("bedroom_1", 0, 1, info_heater_1),
"light_2" : powerConsumer("bedroom_2", 40, 1, info_light_2),
"curtains_2" : powerConsumer("bedroom_2", 0, 1, info_curtains_2),
"heater_2" : powerConsumer("bedroom_2", 0, 1, info_heater_2),
"light_3" : powerConsumer("bedroom_3", 40, 1, info_light_3),
"curtains_3" : powerConsumer("bedroom_3", 0, 1, info_curtains_3),
"heater_3" : powerConsumer("bedroom_3", 0, 1, info_heater_3),
"light_4" : powerConsumer("bedroom_4", 40, 1, info_light_4),
"curtains_4" : powerConsumer("bedroom_4", 0, 1, info_curtains_4),
"heater_4" : powerConsumer("bedroom_4", 0, 1, info_heater_4),
}

rooms = {
"Total" : consumers,
"livingroom" : [],
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
                print (consumerList[i].room)
                roomList[key].append(consumerList[i])


def updateConsumerStatus(dictionary): # Oppdaterer de ulike objektene sin powerStatus (Av/PÅ) fra CoT
    for i in dictionary:
        dictionary[i].status()


def logThis(consumerList, roomList) : #skriver forbruket til csv.fil. Tar inn dictionary med frobrukere og romliste
    for key in roomList.keys() :
        print (key)
        for i in roomList[key] :
            print (i)
            print (roomList[key][i])
            Consumption = 0
            if roomList[key][i].status() == 1 :
                Consumption += roomList[key][i].effect
            else : 
                pass     

def initCsv(roomList) :
    listOfCSVHeaders = ["Time"]
    for key in roomList :
        listOfCSVHeaders.append(roomlist[key])
    with open ("powerUsage.csv", "a", newline="") as f:
        csvReader = csv.DictReader
# LEGGE TIL HEADER I CSV FILA



def powerConsumptionLogging(room, consumption): #Funksjon for å skrive til en .csv fil
    kW = consumption/1000 # Gjør om til kiloWatt
    now = time.strftime('%d-%m-%Y %H:%M:%S')
    print("The time is" + now)
    with open("powerUsage.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, str(kW)])

putObjectsInRooms(consumers, rooms)
logThis(consumers, rooms)

# CSV file layout:
# TIME, TOTAlConsumption, livingroom, Kitchen, Bathroom, bedroom_1, bedroom_2, bedroom_3, bedroom_4, solarPanel, TotalCost, SolarPanelSavings


""" Hvordan få justert effektforbruket etter utetemperatur og tid på  døgnet? """

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