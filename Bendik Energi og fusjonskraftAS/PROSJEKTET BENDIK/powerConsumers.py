import time 
import requests
import json
import pandas as pd
import csv
import key as key #Personlige tokens
import random # MIDLERTIDIG


token = key.token # Henter CoT Token fra key.py fil
api_key = key.api_key # Token til ENTSOE fra key.py


class powerConsumer: # Klassen til alle strømforbrukennde apparater i leiligheten. 
    def __init__(self, room, effect, numOfUses, payload ) :# Rom, forbruk i watt, antall bruk før kjøring, kommunikasjonsnøkkel
        self.room = room
        self.effect = effect
        self.numOfUses = numOfUses
        self.payload = payload
        self.timesUsed = 0
        self.currentState = 0
        self.previousState = 0

    def status(self) : 
        """ 
            Henter AV/PÅ status fra CoT 
            Oppdaterer forrige status for å sjekke antall bruk
            Returnerer value fra CoT-respons
        """
        response = requests.get("https://circusofthings.com/ReadValue", params = self.payload) # Body for request
        self.previousState = self.currentState # Oppdaterer forrige status     
        self.currentState = json.loads(response.content)["Value"] # Leser verdi fra CoT respons
        return json.loads(response.content) # returnerer 

    def powerOn(self): 
        """ 
        Sjekker hvor mange ganger apparatet er blitt brukt
            og om det skal registreres som aktivt ved oppdatert signal
        """
        power = 0
        if self.numOfUses > 1:
            self.timesUsed = self.timesUsed+1
            if self.currentState != self.previousState:
                if self.timesUsed > self.numOfUses:
                    self.timesUsed = 0   
                if self.timesUsed == self.numOfUses:
                    power = self.effect
        if self.currentState == 1:
                power = self.effect
        return power

    def changeEffect(self) :
        """ 
        Endre forbrukt effekt hos enkelte av apparatene som varmekabler i huset. 
         """
        self.effect = 1


    def updateState(self, newState):
        """ 
        Sender ny status til CoT
         """
        dataDict = self.payload
        dataDict["Value"] = newState
        response = requests.put("https://circusofthings.com/WriteValue", data=json.dumps(dataDict),headers={'Content-Type':'application/json'} )
        return json.loads(response.content)



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

consumers = { 
""" 
Definerer ulike strømforbrukende apparater 
Legg inn nye objekter her:
"""

"livingroomLight" : powerConsumer("livingroom", 40, 1, info_livingRoomLight),
"TV" : powerConsumer("livingroom", 10, 1, info_TV),
"LivingroomHeater" : powerConsumer("livingroom", 1000, 1, info_TV), #BYTT UT COT-KODE
"stove" : powerConsumer("kitchen", 2200, 1, info_stove),
"dishwasher" : powerConsumer("kitchen",2000, 4, info_dishwasher),
"coffeeMachine" : powerConsumer("kitchen", 1500, 1, info_coffeeMachine),
"fridge" : powerConsumer("kitchen", 160, 1, info_fridge),
"kitchenHeater" : powerConsumer("kitchen", 1000, 1, info_kitchenHeater), #Sjekk i COT
"kitchenLight" : powerConsumer("kitchen", 40, 1, info_kitchenLight),
"washingMachine" : powerConsumer("bathroom", 2500, 4, info_washingMachine),
"shower" : powerConsumer("bathroom", 1000, 1, info_shower),
"heatingCable" : powerConsumer("bathroom", 1500, 1, info_heatingCable),#Sjekk i COT
"light_1" : powerConsumer("bedroom_1", 40, 1, info_light_1),
"curtains_1" : powerConsumer("bedroom_1", 10, 1, info_curtains_1),
"heater_1" : powerConsumer("bedroom_1", 1000, 1, info_heater_1),
"light_2" : powerConsumer("bedroom_2", 40, 1, info_light_2),
"curtains_2" : powerConsumer("bedroom_2", 10, 1, info_curtains_2),
"heater_2" : powerConsumer("bedroom_2", 1000, 1, info_heater_2),
"light_3" : powerConsumer("bedroom_3", 40, 1, info_light_3),
"curtains_3" : powerConsumer("bedroom_3", 10, 1, info_curtains_3),
"heater_3" : powerConsumer("bedroom_3", 1000, 1, info_heater_3),
"light_4" : powerConsumer("bedroom_4", 40, 1, info_light_4),
"curtains_4" : powerConsumer("bedroom_4", 10, 1, info_curtains_4),
"heater_4" : powerConsumer("bedroom_4", 1000, 1, info_heater_4),
}

rooms = {
"Total" : consumers,
"livingroom" : {},
"kitchen" : {},
"bathroom" : {},
"bedroom_1" : {},
"bedroom_2" : {},
"bedroom_3" : {},
"bedroom_4" : {},
"CostOfPower" : {},
"solarPanels" : {}, # kwH power generated 
"solarSavings" : {}, # kwh converted to money saved
}


def putObjectsInRooms(consumerList, roomList) :
    """ 
    Funksjon for å sortere alle apparatene inn i riktig rom basert på hvilket rom de ble innitsialisert med. 
    """
    for key in roomList.keys() :
        for i in consumerList :
            if consumerList[i].room == key :
                roomList[key].update({i : consumerList[i]})

def updateConsumerStatus(dictionary): 
    """ 
    Oppdaterer status (Av/På) til alle apparater i gitt dictionary. 
    """
    for i in dictionary:
        dictionary[i].status()

def setConsumerStatus(newValue, roomlist) :
    for key in roomlist.keys() :
        for i in roomlist[key] :
            roomlist[key][i].updateState(newValue)



def initCsv(roomlist) :     #Sjekke for, og legge til header i CSV fil basert på hva som finnens i roomList
    # Work in Progress. Help ? 
    listOfCSVHeaders = ["Time"]
    for key in roomlist :
        listOfCSVHeaders.append(key) # Lager liste med alle navnene i roomlist
    df = pd.read_csv("powerUsage.csv", header=None)
    df.to_csv("powerUsage.csv", header = listOfCSVHeaders, index=False)

def logThis(consumptionDict,): 
    """ 
    Funksjon for å skrive til en .csv fil
    Tar inn dictionary med {rom : verdi}
    """
    df = pd.DataFrame().from_records([consumptionDict], index =[0])
    df.insert(0, 'timestamp', time.strftime('%d-%m-%Y %H:%M:%S'))
    df.to_csv("powerUsage.csv", mode = 'a', index=False, header = False)

def consumptionLogger(roomList, kWhcompensation) : 
    """ 
    skriver forbruket til csv.fil
    Tar inn dictionary med key : rom, og verdi til strømforbrukende objekt.
    """
    
    consumptionDict = {}
    for key in roomList.keys() :
        consumption = 0
        for i in roomList[key] :
            if roomList[key][i].currentState == 1 :
                consumption += (roomList[key][i].powerOn()*kWhcompensation)/1000 # Deler på 1000 for å få KiloWatt
        consumptionDict.update({key : consumption})
    logThis(consumptionDict)


def randomizeStatus(roomlist) : # RANDOMIZE COT STATUSES.
    for key in roomlist.keys():   
        newValue = random.randint(0,1)
        # print("object is number " + str(key) + " and randomNum is: " + str(newValue))
        roomlist[key].updateState(newValue)



# CSV file layout:
# TIME, TOTAlConsumption, livingroom, Kitchen, Bathroom, bedroom_1, bedroom_2, bedroom_3, bedroom_4, solarPanel, TotalCost, SolarPanel


""" 

Dusj:fastverdi (kWh)> 
Varmekabler på baderom: én kWh-verdi for normal bruk, én for natt-/dagsenking.> 
Stekeplater og stekeovn: forenkles til én kWh-verdi for hver, uansetttype bruk.> 
Panelovner på soverommene: sett opp en enkel modell for kWh-forbruket avhengig av hva termostaten er satt til, 
samt utetemperatur og vindstyrke. Kanskje også sol og 
skydekke, for gruppene som ønsker enekstra utfordring.RPien henter inn værdata.> 
Vaskemaskinen: anta at den kjøres Xganger i uka, og forbrukerYkWh. Videre at hver kjøring avvaskemaskinen følges av kjøring av tørketrommelensomforbrukerZkWh> TVen i TV-stua: anta at dener slått på med et forbruk på XkWhså lenge TV-stua er booket.> 
Oppvaskmaskinen:Én frokost fyller 10%, én lunsj 15%og én middag 25%. Forbruket er XkWh for hver kjøring. Denkjører når fyllingsgraden er>90%og < 100%-Modellereproduksjonen:>
Solcellepanelet:produksjonenavhenger av solcelletypen (plukk et konkret panel og sjekk databladet), virkningsgraden, solens posisjon, skydekke, lufttemperatur,etc.RPienhenter inn værdata.

"""