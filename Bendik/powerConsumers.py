import time
import requests
import json
import pandas as pd
import csv
import key as key #Personlige tokens
import random # MIDLERTIDIG
import currency
import weatherData as WD
import solarPanel as SP

token = key.token # Henter CoT Token fra key.py fil
api_key = key.api_key # Token til ENTSOE fra key.py


class rooms:
    def __init__(self, area, height,) :
        self.area = area
        self.height = height

    def volume(self):
        return (self.area * self.height)

###___ Angir størrelsen til rommene ___###
### Areal * høyde
livingroom = rooms(25, 3)
kitchen =  rooms(15, 3)
bathroom = rooms(12, 3)
bedroom_1 = rooms(10, 3)
bedroom_2 = rooms(10, 3)
bedroom_3 = rooms(10, 3)
bedroom_4 = rooms(10, 3)
bedroom_5 = rooms(10, 3)
bedroom_6 = rooms(10, 3)


class powerConsumer:
    """ 
    Klassen til alle strømforbrukennde apparater i leiligheten.
    Initialiseres med Rom, forbruk (i watt), antall bruk før kjøring, kommunikasjonsnøkkel til CoT

    """ 
    def __init__(self, room, effect, numOfUses, payload ) :
        self.room = room
        self.effect = effect
        self.numOfUses = numOfUses
        self.payload = payload
        self.timesUsed = 0
        self.currentState = 0
        self.previousState = 0
        self.currentTemp = 0
        self.previousTemp = 0

    def status(self) : 
        """ 
            Henter AV/PÅ status fra CoT 
            Oppdaterer forrige status for å sjekke antall bruk
            Returnerer value fra CoT-respons
        """
        response = requests.get("https://circusofthings.com/ReadValue", params = self.payload) # Body for request
        self.previousState = self.currentState # Oppdaterer forrige status     
        # print(response.content) # FOR debug
        self.currentState = json.loads(response.content)["Value"] # Leser verdi fra CoT respons
        return json.loads(response.content) # returnerer 


    def adjustConsumption(self) :
        """ 
        Endre forbrukt effekt hos enkelte av apparatene, som varmekabler i huset.
        Sjekker om status i CoT er høyere enn 1, og antar at den gitte verdien er ønsket temperatur.

        Returnerer den prosentvise endringen i temperatur

        """
        if self.currentState > 1:
            targetTemp = self.currentState
            self.currentTemp = self.currentState
            tempDelta = (self.previousTemp - targetTemp)
            self.previousTemp = self.currentTemp
            outsideTemp = WD.getTemperature() # Henter værdata fra weatherStation pakken som ble bygd for prosjektet. 
            if  outsideTemp > targetTemp: 
                return 0.1 # Varmekabler slås ikke helt av, men forbruker mindre strøm når det er varmt ute. 
            if outsideTemp < targetTemp:      
                if tempDelta >= 0:
                    minTemp, maxTemp = 10, 25
                    range = maxTemp - minTemp
                    correctedStartValue = self.currentTemp - minTemp
                    return (correctedStartValue * 100) / range 
                else:
                    return 1
        else:
            return 1
        
    
    def powerOn(self): 
        """ 
        Sjekker hvor mange ganger apparatet er blitt brukt
        og om det skal registreres som aktivt ved oppdatert signal
        """
        power = 0
        if self.numOfUses > 1:
            """  For de apparatene som må brukes flere ganger før de kjøres """
            self.timesUsed = self.timesUsed+1
            if self.currentState != self.previousState:
                if self.timesUsed > self.numOfUses:
                    self.timesUsed = 0   
                if self.timesUsed == self.numOfUses:
                    return (self.effect)
        if self.currentState >= 2:
            """  
                For apparater som skal skrus av eller på, 
                eller få justert effektforbruket prosentvis.  
            """
            #print (self.adjustConsumption())
            return (self.effect * self.adjustConsumption()) / 100 # Korrigerer strømforbruk etter ønsket temperatur
        if self.currentState == 1:
            power = self.effect
        return power



    def updateState(self, newState):
        """ 
        Sender ny status til CoT dersom det er en endring i egen tilstand 
        Til bruk ved simulering. 
         """
        self.currentState = newState # Sikrer at ett objekt aldri står på i mer enn en tidsenhet minutter(Dusj, kaffetrakter etc)
        if newState != self.previousState : # Avoids unneccesary updates to CoT
            dataDict = self.payload
            dataDict["Value"] = newState
            response = requests.put("https://circusofthings.com/WriteValue", data=json.dumps(dataDict),headers={'Content-Type':'application/json'} )
            #return json.loads(response.content) # For feilsøking


# Definerer "kontaktinfo" til apparatene i CoT
info_TV = {'Key':'24411','Value':0,'Token':token}
info_livingRoomLight = {'Key':'21989','Value':0,'Token':token}
info_LivingroomTemp = {'Key':'21771','value':0,'Token':token} 
info_stove = {'Key':'26299','Value':0,'Token':token} 
info_dishwasher = {'Key':'22562','Value':0,'Token':token} 
info_coffeeMachine = {'Key':'9242','Value':0,'Token':token} 
info_fridge = {'Key':'18863','Value':0,'Token':token}
info_kitchenHeater = {'Key':'3714','Value':0,'Token':token} 
info_kitchenLight = {'Key':'8485','Value':0,'Token':token} 
info_shower = {'Key':'29262','Value':0,'Token':token} 
info_washingMachine = {'Key':'28922','Value':0,'Token':token} 
info_bathroomTemp = {'Key':'373','Value':0,'Token':token}
info_bathroomLight = {'Key':'29768', 'Value':0,'Token':token} ### ??!!???!!
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
info_light_5 = {'Key':'16956','Value':0,'Token':token}
info_curtains_5 = {'Key':'8365','Value':0,'Token':token}
info_heater_5 = {'Key':'18377','Value':0,'Token':token}
info_light_6 = {'Key':'29556','Value':0,'Token':token}
info_curtains_6 = {'Key':'8365','Value':0,'Token':token}
info_heater_6 = {'Key':'14945','Value':0,'Token':token}
# LEGG TIL KEY for  CURTAINS


consumers = { 
""" 
Definerer ulike strømforbrukende apparater 
Legg inn nye objekter her:
"""

"livingroomLight" : powerConsumer("livingroom", 40, 1, info_livingRoomLight),
"TV" : powerConsumer("livingroom", 150, 1, info_TV),
"LivingroomTemp" : powerConsumer("livingroom", 1500, 1, info_TV), #BYTT UT COT-KODE
"Stove" : powerConsumer("kitchen", 2200, 1, info_stove),
"Dishwasher" : powerConsumer("kitchen",2000, 4, info_dishwasher),
"CoffeeMachine" : powerConsumer("kitchen", 1500, 1, info_coffeeMachine),
"Fridge" : powerConsumer("kitchen", 160, 1, info_fridge),
"KitchenTemp" : powerConsumer("kitchen", 1500, 1, info_kitchenHeater), #Sjekk i COT
"KitchenLight" : powerConsumer("kitchen", 40, 1, info_kitchenLight),
"WashingMachine" : powerConsumer("bathroom", 2500, 4, info_washingMachine),
"Shower" : powerConsumer("bathroom", 1000, 1, info_shower),
"BathroomTemp" : powerConsumer("bathroom", 1500, 1, info_bathroomTemp),#Sjekk i COT
"BathroomLight" : powerConsumer("bathroom", 40, 1, info_bathroomLight),
"Light_1" : powerConsumer("bedroom_1", 40, 1, info_light_1),
"Curtains_1" : powerConsumer("bedroom_1", 10, 1, info_curtains_1),
"Bedroom_1Temp" : powerConsumer("bedroom_1", 1500, 1, info_heater_1),
"Light_2" : powerConsumer("bedroom_2", 40, 1, info_light_2),
"Curtains_2" : powerConsumer("bedroom_2", 10, 1, info_curtains_2),
"Bedroom_2Temp" : powerConsumer("bedroom_2", 1500, 1, info_heater_2),
"Light_3" : powerConsumer("bedroom_3", 40, 1, info_light_3),
"Curtains_3" : powerConsumer("bedroom_3", 10, 1, info_curtains_3),
"Bedroom_3Temp" : powerConsumer("bedroom_3", 1500, 1, info_heater_3),
"Light_4" : powerConsumer("bedroom_4", 40, 1, info_light_4),
"Curtains_4" : powerConsumer("bedroom_4", 10, 1, info_curtains_4),
"Bedroom_4Temp" : powerConsumer("bedroom_4", 1500, 1, info_heater_4),
"Light_5" : powerConsumer("bedroom_5", 40, 1, info_light_4),
"Curtains_5" : powerConsumer("bedroom_5", 10, 1, info_curtains_4),
"Bedroom_5Temp" : powerConsumer("bedroom_5", 1500, 1, info_heater_4),
"Light_6" : powerConsumer("bedroom_6", 40, 1, info_light_4),
"Curtains_6" : powerConsumer("bedroom_6", 10, 1, info_curtains_4),
"Bedroom_6Temp" : powerConsumer("bedroom_6", 1500, 1, info_heater_4),
}

rooms = {
"Total" : consumers,
"Livingroom" : {},
"Kitchen" : {},
"Bathroom" : {},
"Bedroom_1" : {},
"Bbedroom_2" : {},
"Bedroom_3" : {},
"Bedroom_4" : {},
"Bbedroom_5" : {},
"Bedroom_6" : {},
"CostOfPower" : {}, # Price per kWh
"SolarPanels" : {}, # kwH power generated 
"SolarSavings" : {}, # kwh converted to money saved
"TotalExSolar" : consumers,
}

###___ Funksjoner knyttet til dictionaries ____###


def placeObjectsInRooms(consumerList, roomList) :
    """ 
    Funksjon for å sortere alle apparatene inn i riktig rom basert på hvilket rom de ble innitsialisert med. 
    """
    print("Placing Objects in desiered rooms")
    for key in roomList.keys() :
        for i in consumerList :
            if consumerList[i].room == key :
                """ print(consumerList[i].room)
                print(key) """
                roomList[key].update({i : consumerList[i]})

def updateConsumerStatus(dictionary): 
    """ 
    Oppdaterer status (Av/På) til alle apparater i gitt dictionary. 
    """
    print("Updating Consumer objects status from COT...")
    for i in dictionary:
        #print(dictionary[i])
        dictionary[i].status()

def setConsumerStatus(newValue, roomlist) :
    """ 
    Oppdaterer alle objektene i romlisten med identisk, ny verdi. 
    Må ta inn dictionary med powerConsumer objekter. 
    """
    print("Pushing new state to COT.......")
    for key in roomlist.keys() :
        for i in roomlist[key] :
            roomlist[key][i].updateState(newValue)

###___ Funksjoner for logging av strømforbruk ___###


def initCsv(roomlist) :    
    """
    Legger til header i CSV fil basert på hva som finnens i roomList. 
    Obs! Sjekker ikke om header eksisterer fra før. 
    """
    listOfCSVHeaders = ["Time"]
    for key in roomlist :
        listOfCSVHeaders.append(key) # Lager liste med alle navnene i roomlist
    df = pd.read_csv("powerUsage.csv", header=None)
    df.to_csv("powerUsage.csv", header = listOfCSVHeaders, index=False)

initCsv(rooms)

def logThis(df): 
    """ 
    Funksjon for å skrive til en .csv fil
    Tar inn en pandas dataframe
    """
    df.insert(0, 'timestamp', time.strftime('%d-%m-%Y %H:%M:%S'))
    df.to_csv("powerUsage.csv", mode = 'a', index=False, header = False)

def logThisDemo(df): 
    """ 
    Funksjon for å skrive til en .csv fil
    Lagrer med timeStep istedenfor tid. 

    FIKS! 
    """
    df.insert(0, 'timestamp', time.strftime('%d-%m-%Y %H:%M:%S'))
    df.to_csv("powerUsage.csv", mode = 'a', index=False, header = False)


def toDF(dict) :
    df = pd.DataFrame().from_records([dict], index =[0])
    return df


def consumptionLogger(roomList, kWhcompensation, start, end) : 
    """ 
    Henter forbruket fra alle apparater
    Tar inn dictionary med key : rom, en tidskonstant for kWh beregning, start og sluttid.
    """
    
    consumptionDict = {}
    date = '14-05-2021'

    print("Writing to csv...")
    for key in roomList.keys() :
        consumption = 0
        for i in roomList[key] :
            #print("Printing consumption for: " + str(i))
            consumption += (roomList[key][i].powerOn()*kWhcompensation)/1000 # Deler på 1000 for å få KiloWatt           
            #print(consumption)
        consumptionDict.update({key : consumption})

    solarPanels = (SP.solarPanelPower(date, SP.getIndexIntoDay())/1000) # Converts into KiloWatt
    powerPrice = currency.powerPriceInNok(start, end)
    solarSavingns = (solarPanels * powerPrice)
    calculatedTotal = (consumptionDict["Total"] - solarPanels)

    consumptionDict.update({"costOfPower" : powerPrice})  
    consumptionDict.update({"solarPanels" : solarPanels}) 
    consumptionDict.update({"solarSavings" : solarSavingns}) 
    consumptionDict.update({"Total" : calculatedTotal }) 

    DF = toDF(consumptionDict)
    logThis(DF)


def randomizeStatus(roomlist) :
     # RANDOMIZE COT STATUSES.
    for key in roomlist.keys():   
        newValue = random.randint(0,1)
        # print("object is number " + str(key) + " and randomNum is: " + str(newValue))
        roomlist[key].updateState(newValue)






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


""" C = 1.006 # dry air specific heat, J/g K
                p = 1275 # dry air density. g/m3
                v = self.room.volume()
                U = C * p * v * tempDelta # requered effect in KiloJoule to change temperature
                kwH = U/0.277777778 # Covnert from Kilo Joule to Kilo Watt  """