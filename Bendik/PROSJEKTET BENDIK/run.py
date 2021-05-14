import powerConsumers
import time 
import solarPanel
import weatherStation_Trondheim



timeInterval = 10
startTime = "20210413"
endTime = "20210414"

def timePassed(oldTime, interval) :
    if time.time() - oldTime >= interval:
        return True
    else:
        return False

powerConsumers.placeObjectsInRooms(powerConsumers.consumers, powerConsumers.rooms)
oldTime = time.time()
n = 0
while (n < 50) :  # Enkel løkke for å generere 50 linjer med data 
    if timePassed(oldTime, timeInterval) == True :
        oldTime = time.time()
        n += 1
        #powerConsumers.randomizeStatus(powerConsumers.consumers) # Gir tilfeldig verdi til CoT objektene 
        powerConsumers.updateConsumerStatus(powerConsumers.consumers) # Henter inn ny status 
        powerConsumers.consumptionLogger(powerConsumers.rooms, timeInterval, startTime, endTime) # SKriver til CSV fil 

        
        print(n)  #Sjekker iterasjon i løkka 
