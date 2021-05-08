import powerConsumers
import time 

timeInterval = 40


def timePassed(oldTime, interval) :
    if time.time() - oldTime >= interval:
        return True
    else:
        return False

powerConsumers.putObjectsInRooms(powerConsumers.consumers, powerConsumers.rooms)
oldTime = time.time()
n = 0
while (n < 50) :  # Enkel løkke for å generere 50 linjer med data 
    if timePassed(oldTime, timeInterval) == True :
        oldTime = time.time()
        n += 1
        powerConsumers.randomizeStatus(powerConsumers.consumers) # Gir tilfeldig verdi til CoT objektene 
        powerConsumers.updateConsumerStatus(powerConsumers.consumers) # Henter inn ny status 
        powerConsumers.consumptionLogger(powerConsumers.rooms, timeInterval) # SKriver til CSV fil 
        print(n)  #Sjekker iterasjonn i løkka 
