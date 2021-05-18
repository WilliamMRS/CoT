import powerConsumers
import time 

def timePassed(oldTime, interval) :
    if time.time() - oldTime >= interval:
        return True
    else:
        return False

timeInterval = 60

startTime = "20210413"
endTime = "20210414"



powerConsumers.placeObjectsInRooms(powerConsumers.consumers, powerConsumers.rooms)
oldTime = time.time()
n = 0


#powerConsumers.initCsv(powerConsumers.rooms) # For setting header in .csv file

while (n < 50) :  # Enkel løkke for å generere 50 linjer med data med gitt tidsintervall 
    if timePassed(oldTime, timeInterval) == True :
        oldTime = time.time()
        n += 1
        powerConsumers.updateConsumerStatus(powerConsumers.consumers) # Henter inn ny status 
        powerConsumers.consumptionLogger(powerConsumers.rooms, timeInterval, startTime, endTime) # SKriver til CSV fil 

        print ("num of times loop: ")
        print(n)  #printer iterasjon i løkka 



