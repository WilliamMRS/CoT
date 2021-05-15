import requests
import time
import pandas as pd
import powerConsumers as pc
import booking_functions as bf
import os

def bookRoom(rom, start, slutt, bruker): # 0-2, 11:00, 12:00, 1-6    // Dette er eksempel inputs
    url = 'http://localhost:5000/api/bookRoom'
    myobj = {
        'room_form': rom, # id: 0 er bad, 1 er stue, 2 er kjøkken
        'time_start': start, # start time
        'time_end': slutt, # end time
        'user_name': bruker # id of user
    }
    x = requests.post(url, data = myobj)
    print(x.text)
# Start tid 00:00 AM
# Book alle rommene som skal brukes av folk

def timePassed(oldTime, interval) :
    if time.time() - oldTime >= interval:
        return True
    else:
        return False

def getRoomOccupants(index, room): # Takes index between 0 and 143, 10 minute intervals in 24hrs ---- 0: bad, 1: stue, 2: kjøkkenet
    index = index*2
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../server/booking.csv')
    df =  bf.csvToDf(filename)
    
    users = []
    if room == "Bathroom":
        for userid in df["Bathroom"][index]:
            if userid != "[" and userid != "]":
                users.append(userid)
    elif room == "Livingroom":
        for userid in df["Livingroom"][index]:
            if userid != "[" and userid != "]":
                users.append(userid)
    elif room == "Kitchen":
        for userid in df["Kitchen"][index]:
            if userid != "[" and userid != "]":
                users.append(userid)
    return users

#print(getRoomOccupants(90, 0)) # Takes index and roomID

def timeIndex():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, now.day)
    diff = now - start
    seconds_in_day = 24 * 60 * 60
    return int((144 / seconds_in_day) * diff.seconds) # converts seconds to intervals of 144 (10 min) and throws away decimal.


def indexOfDay(index) :
    #____ Checks if its nighttime and returns True
    if index in range(0, 35) or index in range (110, 144):
       return True
