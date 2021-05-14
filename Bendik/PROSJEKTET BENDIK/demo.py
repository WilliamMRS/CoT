## DEMOSKRIPT

import powerConsumers as pc
import time

""" Alle tilgjengelige apparater: 
Oppdater tilstand med pc.consumers["apparatnavn"].updateState(NewState)

ex. pc.consumers["stove"].updateState(1) for å skru på ovn. 

# Stue
    "livingroomLight", "TV" , "LivingroomTemp"
# Kitchen: 
    "stove" , "dishwasher" , "coffeeMachine", "fridge", "kitchenTemp",
    "kitchenLight" 
# Bad:      
    "washingMachine", "shower", "bathroomTemp", "bathroomLight"
#Sov1:
    "light_1" , "curtains_1", "bedroom_1Temp" 
#Sov2 : 
    "light_2" , "curtains_2" , "bedroom_2Temp" 
# Sov 3:
    "light_3", "curtains_3" , "bedroom_3Temp" 
# Sov 4:
    "light_4" , "curtains_4", "bedroom_4Temp"
# Sov 5:
    "light_5" , "curtains_5", "bedroom_5Temp"
#Sov6:
    "light_6" , "curtains_6", "bedroom_6Temp" 


"""

###___ Initialisering ___ ### 


timeInterval = 30 # Endre hyppighet for logging i sekunder

pc.placeObjectsInRooms(pc.consumers, pc.rooms) # Initialiserer alle objektene. 
oldTime = time.time()
startTime = "20210513"
endTime = "20210514"

###___ Løkke___###

while () :  # Kondisjon for å skru av og på?
    if pc.timePassed(oldTime, timeInterval) == True :
        oldTime = time.time()
        pc.updateConsumerStatus(pc.consumers) # Henter inn ny status 
        pc.consumptionLogger(pc.rooms, timeInterval, startTime, endTime) # SKriver til CSV fil 


# Booking

# Strømforbruk følger booking. 


# Ting skrur seg av å på etter hvor folk er.     Bruksmønster

    # Lys følger alltid booking
    # Temperatur i stue, kjøkken, bad  settes til 21 grader så lenge det er folk der. 
        # Skrus ned til 18 når det ikke er noen der. 

    # Bad
        # hver tredje gang noen er på badet brukes dusjen i 10 minutter
        # Temperatur satt til 23 grader på dagtid
        # Temperatur satt til 17 grader på natt. 

    # Kjøkken
        # Hver gang noen er på kjøkkenet brukes vaskemaskinen. 
            # Den skrus automatisk på etter å ha fått endret status fem ganger. 
            # La den stå på i 60 minutter den 5. gangen.
        # Kaffetrakter brukes hver 5 gang noen er på kjøkkenet
        # Kjøleskap står alltid på
        # Ovn brukes 3. hver gang noen er på kjøkkenet. 

    # Soverom
        # Temperatur på soverom settes til 18 grader om kvelden. 21 på dagtid dersom noen er der.
        # For å spare signaler har alle gardiner samme kode. 
            # Sett disse til å heve senke ved legge- / våknetid? Evt. bare dropp de. 
    # Stue
        # TV skrus på når noen er i stua







