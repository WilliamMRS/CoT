## DEMOSKRIPT
import powerConsumers as pc
import time
import demo_functions as defunc
import demoBooking as debok
import csv
from booking_functions import clearCSV

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

# ----------------
    # Initialisering
# ----------------

print ("Initializing......")
timeInterval = 60 # Endre hyppighet for logging i sekunder

pc.placeObjectsInRooms(pc.consumers, pc.rooms) # Initialiserer alle objektene. 
oldTime = time.time()

startTime = "20210513" # For strømpris og valuttakurs
endTime = "20210514" # For strømpris og valuttakurs

bookingRooms = ["Bathroom", "Livingroom", "Kitchen"]
idleTemp = 16
useTemp = 22
kitchenUses, bathroomUses, livingroomUses = 0, 0, 0 # For keeping track of num of Uses of a room during a day. 




# ----------------
    #Bookings
# ----------------
            # add all bookings planned for today
            # Gjnnomføres i egen fil

#clearCSV("../server/booking.csv")
#debok.bookAllTheRooms()

# ----------------
    # USAGE CONDITIONS
# ----------------
print("Starting demo......")


for index in range (0, 143): # index = timeIntervall 1-144 
    userLocation = { # For placing people in their own room as baseline
        "Livingroom" : {},
        "Kitchen" : {},
        "Bathroom" : {},
        "Bedroom_1" : {"[1]"},
        "Bedroom_2" : {"[2]"},
        "Bedroom_3" : {"[3]"},
        "Bedroom_4" : {"[4]"},
        "Bedroom_5" : {"[5]"},
        "Bedroom_6" : {"[6]"},
    }
    pc.setConsumerStatus(0, pc.rooms) #Forces all objects to off state before checking who need to be turned on
    for room in bookingRooms:
        # Lower temperature inn all rooms before checking if there is people there
            pc.consumers[str(room)+"Temp"].updateState(idleTemp)
    for room in bookingRooms:
        users = defunc.getRoomOccupants(index, bookingRooms) #Function returns a list of people in the given room 
        print (users)
        for num in range(1, 7): # 1-6 for 6 personer.
            if num in users:
                    userLocation.pop(room) # Fjerner personer fra rom der de ikke befinner seg lengre.    
        for user in users:
            userLocation.update({room : user}) # Legger til personer i korrekt rom. 
        


    for key in userLocation : 
    #______ Sjekker hvilket rom personer er plassert i og om eventuelle apparater skal skrus på ______#
        if len(userLocation[key]) > 0 : # Sjekker om det befinner seg personer i rommet. 
        
            if key == "Livingroom" : 
                livingroomUses += 1
                pc.consumers["livingroomTemp"].updateState(useTemp)
                pc.consumers["TV"].updateState(1)

            if key == "Bathroom" :
                bathroomUses += 1
                pc.consumers["bathroomTemp"].updateState(23)
                if index in range(35, 54) or index in range (108, 112) :
                    # If morning or early evening. Assume people is going to the shower while visiting the bathroom 
                    pc.consumers["shower"].updateState(1) 
            
            if key == "Kitchen" :
                kitchenUses += 1
                pc.consumers["KitchenTemp"].updateState(useTemp)
                pc.consumers["Dishwasher"].updateState(1)
                if kitchenUses % 4 == 0:
                    pc.consumers["CoffeMachine"].updateState(1)
                if kitchenUses % 3 == 0:
                    pc.consumers["Stove"].updateState(1)

            if key == "Bedroom_1" :
                if defunc.indexOfDay(index) :
                    pc.consumers[str(key)+"Temp"].updateState(idleTemp)
                    pc.consumers["Curtains_1"].updateState(1)
                else:
                    pc.consumers[str(key)+"Temp"].updateState(useTemp)

            if key == "Bedroom_2" :
                if defunc.indexOfDay(index) :
                    pc.consumers[str(key)+"Temp"].updateState(idleTemp)
                    pc.consumers["Curtains_2"].updateState(1)
                else:
                    pc.consumers[str(key)+"Temp"].updateState(useTemp)
            
            if key == "Bedroom_3" :
                if defunc.indexOfDay(index) :
                    pc.consumers[str(key)+"Temp"].updateState(idleTemp)
                    pc.consumers["Curtains_3"].updateState(1)
                else:
                    pc.consumers[str(key)+"Temp"].updateState(useTemp)
                    pc.consumers["Curtains_1"].updateState(1)
           
            if key == "Bedroom_4" :
                if defunc.indexOfDay(index) :
                    pc.consumers[str(key)+"Temp"].updateState(idleTemp)
                    pc.consumers["Curtains_4"].updateState(1)
                else:
                    pc.consumers[str(key)+"Temp"].updateState(useTemp)
       
            if key == "Bedroom_5" :
                if defunc.indexOfDay(index) :
                    pc.consumers[str(key)+"Temp"].updateState(idleTemp)
                    pc.consumers["Curtains_5"].updateState(1)
                else:
                    pc.consumers[str(key)+"Temp"].updateState(useTemp)
       
            if key == "Bedroom_6" :
                if defunc.indexOfDay(index) :
                    pc.consumers[str(key)+"Temp"].updateState(idleTemp)
                    pc.consumers["Curtains_6"].updateState(1)
                else:
                    pc.consumers[str(key)+"Temp"].updateState(useTemp)      
    pc.consumers["Fridge"].updateState(1) # Ensures that Fridge always will be on
    print("This is INDEX RUN NR: ")
    print (index)


# ----------------
    # CHECKS COT STATUS & LOGS
# ----------------

    if defunc.timePassed(oldTime, timeInterval) == True :
        oldTime = time.time()
        pc.updateConsumerStatus(pc.consumers) # Henter inn ny status 
        pc.consumptionLogger(pc.rooms, timeInterval*20, startTime, endTime) # Skriver til CSV fil 

    with open('user_locations.csv', 'w', newline='') as csvfile:
        fieldnames = ["Livingroom","Kitchen","Bathroom","Bedroom_1","Bedroom_2","Bedroom_3","Bedroom_4","Bedroom_5","Bedroom_6"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(userLocation)


# Dersom brukerID ikke er på ett annet rom antar vi at ID er på eget rom 

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
        # Temperatur på soverom settes til 17 grader om kvelden. 21 på dagtid dersom noen er der.
        # For å spare signaler har alle gardiner samme kode. 
            # Sett disse til å heve senke ved legge- / våknetid? Evt. bare dropp de. 
    # Stue
        # TV skrus på når noen er i stua


