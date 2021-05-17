## DEMOSKRIPT
import csv
import time

import demo_functions as defunc
import demoBooking as debok
import powerConsumers as pc
from booking_functions import clearCSV


# ----------------
    # Initialisering
# ----------------

print ("Initializing......")



pc.placeObjectsInRooms(pc.consumers, pc.rooms) # Initialiserer alle objektene. 


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


clearCSV("../server/booking.csv")
debok.bookAllTheRooms()

# ----------------
    # USAGE CONDITIONS
# ----------------
print("Starting demo......")

loops = 144
timeInterval = 24/loops #approx 0,16666667
loops = loops-1
# Loop should run 144 times, since 24 hours divided into 10 minute chunks give 144 intervalls. This will also be our time multiplicant for KWh calculations 

for index in range (0, loops): # index = timeIntervall 1-144 
    userLocation = { # For placing people in their own room as baseline
        "Livingroom" : [],
        "Kitchen" : [],
        "Bathroom" : [],
        "Bedroom_1" : {"[1]"},
        "Bedroom_2" : {"[2]"},
        "Bedroom_3" : {"[3]"},
        "Bedroom_4" : {"[4]"},
        "Bedroom_5" : {"[5]"},
        "Bedroom_6" : {"[6]"},
    }

    pc.setConsumerStatus(0, pc.rooms) #Forces all objects to off state before checking who need to be turned on

    pc.consumers["LivingroomTemp"].updateState(idleTemp)
    pc.consumers["KitchenTemp"].updateState(idleTemp)
    pc.consumers["BathroomTemp"].updateState(idleTemp)
    pc.consumers["Bedroom_1Temp"].updateState(idleTemp)
    pc.consumers["Bedroom_2Temp"].updateState(idleTemp)
    pc.consumers["Bedroom_3Temp"].updateState(idleTemp)
    pc.consumers["Bedroom_4Temp"].updateState(idleTemp)
    pc.consumers["Bedroom_5Temp"].updateState(idleTemp)
    pc.consumers["Bedroom_6Temp"].updateState(idleTemp)    

    for room in bookingRooms:
        # Lower temperature inn all rooms before checking if there is people there
        pc.consumers[str(room)+"Temp"].updateState(idleTemp)
        print("setting idle temperature for " + room)

    for room in bookingRooms:
        users = defunc.getRoomOccupants(index, room) #Function returns a list of people in the given room 
        print("Users found", users)
        for num in range(1, 7): # 1-6 for 6 personer.
            if num in users: 
                hybel = "Bedroom_" + str(num)
                userLocation.update({hybel: {}}) # Fjerner personer fra rom der de ikke befinner seg lengre.    
        for user in users:
            print(userLocation[room])
            userLocation[room].append(user) # Legger til personer i korrekt rom.

    for key in userLocation : 
    #______ Sjekker hvilket rom personer er plassert i og om eventuelle apparater skal skrus på ______#

        if len(userLocation[key]) > 0 : # Sjekker om det befinner seg personer i rommet. 
        
            if key == "Livingroom" : 
                livingroomUses += 1
                print(str(key) + " has now been used")
                pc.consumers["LivingroomTemp"].updateState(useTemp)
                pc.consumers["TV"].updateState(1)

            if key == "Bathroom" :
                bathroomUses += 1
                print(str(key) + " has now been used")
                pc.consumers["BathroomTemp"].updateState(23)
                if index in range(35, 54) or index in range (108, 112) :
                    # If morning or early evening. Assume people is going to the shower while visiting the bathroom 
                    pc.consumers["Shower"].updateState(1) 
                if bathroomUses % 3 == 0:
                    pc.consumers["WashingMachine"].updateState(1) 
            
            if key == "Kitchen" :
                kitchenUses += 1
                print(str(key) + " has now been used")
                pc.consumers["KitchenTemp"].updateState(useTemp)
                pc.consumers["Dishwasher"].updateState(1)
                if kitchenUses % 4 == 0:
                    #Antar at 4. hver gang noen bruker kjøkkenet traktes det kaffe. 
                    pc.consumers["CoffeeMachine"].updateState(1)
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
    print("This is INDEX run nr.: " + str(index))


# ----------------
    # CHECKS COT STATUS & LOGS
# ----------------

    pc.updateConsumerStatus(pc.consumers) # Leser av status for alle objekter i COT
    pc.placeObjectsInRooms(pc.consumers, pc.rooms)    
    pc.consumptionLogger(pc.rooms, timeInterval, startTime, endTime) # Skriver til CSV fil etter hvilke rom objektene er plassert i. 

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


