## DEMOSKRIPT
import powerConsumers as pc
import time
import demo_functions as defunc


""" Alle tilgjengelige apparater: Flytt til README?

Oppdater tilstand med pc.consumers["apparatnavn"].updateState(NewState)

ex. 
        pc.consumers["stove"].updateState(1) 
for å skru på ovn. 1 er ny tilstand. Kan være 0 for av, 22 for temperatur. 

# Stue
    "livingroomLight", "TV" , "LivingroomTemp"
# Kitchen: 
    "stove" , "dishwasher" , "coffeeMachine", "fridge", "kitchenTemp",
    "kitchenLight" 
# Bad:
    "washingMachine", "shower", "bathroomTemp", "bathroomLight"
#Sov1:
    "light_1" , "curtains_1", "bedroom_1Temp" 
#Sov2: 
    "light_2" , "curtains_2" , "bedroom_2Temp" 
# Sov 3:
    "light_3", "curtains_3" , "bedroom_3Temp" 
# Sov 4:
    "light_4" , "curtains_4", "bedroom_4Temp"
# Sov 5:
    "light_5" , "curtains_5", "bedroom_5Temp"
#Sov6:
    "light_6" , "curtains_6", "bedroom_6Temp" 

Merk: Alle curtains har samme CoT kode og vil justeres samtidig. 

"""

###___ Initialisering ___ ### 


timeInterval = 30 # Endre hyppighet for logging i sekunder

pc.placeObjectsInRooms(pc.consumers, pc.rooms) # Initialiserer alle objektene. 
oldTime = time.time()

startTime = "20210513" # For strømpris og valuttakurs
endTime = "20210514" # For strømpris og valuttakurs

###___ Løkke___###

while () :  # Kondisjon for å skru av og på?
    if defunc.timePassed(oldTime, timeInterval) == True :
        oldTime = time.time()
        pc.updateConsumerStatus(pc.consumers) # Henter inn ny status 
        pc.consumptionLogger(pc.rooms, timeInterval*20, startTime, endTime) # SKriver til CSV fil 


# Booking og bruksmønster

# alle booker badet fra 07:30 til 09:00, 15 minutter hver.
# folk booker kjøkkenet for en halvtime etter de har vært på badet hver. Det er da alltid bare 2 stk der samtidig. Fra 07:45 til 09:30
# folk booker kjøkkenet for 15 minutter hver, to og to til lunsj. 12:00 til 13:00
# 2 går på toalettet. 13:15 til 13:30
# 4 går på toalettet fra 14:30 til 14:45
# booker kjøkkenet 45 minutter hver, tre og tre. 16:30 til 17:15 og 17:15 til 18:00
# 1,2,4 og 5 bruker stua fra 18:00 til 22:00
# alle booker toalettet for 10 minutter før de legger seg, en og en. Mellom 22:00 og 23:00



# def activateRoom(room) 
#   If one or more is in room. activate
#   return True



# Strømforbruk følger booking. 

# Dersom brukerID ikke er på ett annet rom antar vi at ID er på eget rom 
# Skru av funksjoner på eget rom dersom vedkommende befinnner seg i ett annet rom. 



# Ting skrur seg av å på etter hvor folk er. 

    # Lys følger alltid booking
    # Temperatur i stue, kjøkken, bad  settes til 21 grader så lenge det er folk der. 
        # Skrus ned til 18 når det ikke er noen der. 

    # Bad
        # Temperatur satt til 23 grader på dagtid
        # Temperatur satt til 17 grader på natt. 
        # pc.consumers["bathroomTemp"].updateState(23)
        # pc.consumers["bathroomTemp"].updateState(17)
        # hver tredje gang noen er på badet brukes dusjen i 10 minutter
        # if defunc.timePassed(oldTime, 10) == True :
            #pc.consumers["shower"].updateState(0)


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


