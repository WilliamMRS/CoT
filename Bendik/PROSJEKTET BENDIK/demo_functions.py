import requests
import time
import datetime

def bookRoom(rom, start, slutt, bruker): # 0-2, 11:00, 12:00, 0-6    // Dette er eksempel inputs
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


def getIndexIntoDay():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, now.day)
    diff = now - start
    seconds_in_day = 24 * 60 * 60
    return int((144 / seconds_in_day) * diff.seconds)

""" 
def toTimestep(time)
    # convert 24 hours into 10 min intervall. AKA 144 Timesteps. 

    return step
 """
