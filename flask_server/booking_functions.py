import ast
import csv
import requests
import json
import pandas as pd
import time

#key = 9940
#token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjI4In0.K58Zp9kRjEWJdlIkNRhD2yrV5EB6DcbDRnHsIVRspps"
def getVal(key, token):
    """variable and constants"""
    KEY_1   = key # "9940" -- signal key here  
    TOKEN_1  = token #"eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjI4In0.K58Zp9kRjEWJdlIkNRhD2yrV5EB6DcbDRnHsIVRspps"       #the token is found under account in circusofthings.com

    data_1={'Key':'0','Value':0,'Token':'0'} 
    data_1['Key']=KEY_1 
    data_1['Token']=TOKEN_1


    #-----------------------------------------------------------------------------------------------------------------------#
    """The Get request is shown below"""
    response=requests.get('https://circusofthings.com/ReadValue',params=data_1)

    res = json.loads(response.content) # all information recieved from CoT as a dictionary
    return res['Value']


def time24array(): # lager en liste med tidspunkter fram 24 timer i tid
    import datetime, math

    time = datetime.datetime.now().strftime("%X")
    hour = int(time[0:2])
    if(int(time[4]) >= 5):
        minute = math.floor(int(time[3:5])/10)*10 +5 #forrige 'runde' 5 minutt. eks: kl 20:39 -> 35
    else:
        minute = math.floor(int(time[3:5])/10)*10 #forrige 'runde'  5 minutt. eks: kl 20:34 -> 30

    current_min = minute

    time24h = []

    for n in range(25):
        if n < 24:
            lim = 60
        else:
            lim = current_min
        while minute < lim:
            if len(str(hour)) == 1:
                hour_str = "0" + str(hour)
            else:
                hour_str = str(hour)

            if len(str(minute)) == 1:
                minute_str = "0" + str(minute)
            else:
                minute_str = str(minute)
            
            time24h.append(hour_str + ":" + minute_str)
            
            minute += 5
        minute = 0

        if  hour < 23:
            hour += 1
        else:
            hour = 0
    return time24h

def listDf(df): # gjør at kolonnene med rom inneholder tomme lister (skal brukes til å lagre hvem som har booket hvert rom. Siden hvert rom kan bookes av flere beboere)
    columns = list(df.columns)
    for n in range(1, len(columns)):
        df[columns[n]] = df[columns[n]].astype(object)
        for i in range(len(df[columns[n]])):
            if(type(df[columns[n]][i]) != list):
                #print("notList")
                df[columns[n]][i] = []

def createDf(): #lager en tom df med tidspunkter 24t fram i tid
    columns = ["Time", "Bathroom", "Livingroom", "Kitchen"]
    df = pd.DataFrame(columns=columns)
    df["Time"] = time24array()
    listDf(df) # fyller df-en med tomme lister
    return df

def updateTime(df): # oppdaterer tiden i dataframen
    current_time = time24array()[0] # henter tiden nå
    
    #last_registered_time = df["Time"][0] # sjekker første registrerte tiden i df
    
    delta_timesteps = df.loc[df["Time"] == current_time].index[0] # gir differansen i timesteps fra nåtid og første registrerte tid. eks: nåtid er 15:40, første tid registrert i dfen er 15:30 --> delta_timesteps = 10 [min] / 5 [min/timeStep] = 2[timeStep]
    for column in df:
        df[column] = df[column].shift(-1*delta_timesteps) # oppdaterer hele df-en, slik at vi ikke lagrer data fra fortiden (flytter hver rad delta_timesteps antall "hakk" opp)
    df["Time"] = time24array() #oppdaterer tiden til nåtid (og 24t fram)
    listDf(df)

def booking(df, booking_code): # tar inn en kode på riktig format og booker tilhørende rom
    booking_code = str(booking_code)

    resident = int(booking_code[0])
    room_num = int(booking_code[1])
    start_hour = booking_code[2:4]
    start_minute = booking_code[4:6]
    duration = int(booking_code[6:9])

    start_time = start_hour + ":" + start_minute

    rooms = ["Bathroom", "Livingroom", "Kitchen"] # Bathroom = rom nr. 0, Livingroom = rom nr. 1, Kitchen = rom nr. 2
    maxCapacity = [1, 4, 3] # max antall personer i rommene. samme rekkefølge som over ^^
    
    room_booked = rooms[room_num]
    room_capacity = maxCapacity[room_num] # max antall personer i et rom

    booking_start_index = df.loc[df["Time"] == start_time].index[0]

    if(booking_start_index + int(duration / 5) < df.index[-1]):
        booking_end_index = booking_start_index + int(duration / 5)
    else:
        booking_end_index = df.index[-1] #last index in df
    
    # håndterer feil
    fullyBooked = False
    alreadyBooked = False

    fullyBookedTimes = []
    alreadyBookedTimes = []
    

    for row in range(booking_start_index, booking_end_index): # går gjennom radene som ønskes å bookes og legger til beboeren som booker i listen over hvem som har booket rommet. (Kjører kun dersom personen ikke allerede har booket rommet)
        if((resident in df[room_booked][row]) == False): # sjekker om beboeren allerede har booket rommet
            if (len(df[room_booked][row]) < room_capacity): # sjekker om rommet har ledig kapasitet
                df[room_booked][row].append(resident)
                print("Room booked")
            else:
                fullyBooked = True
                fullyBookedTimes.append(df["Time"][row])
                #print("This room is fully booked")

        else:
            alreadyBooked = True
            alreadyBookedTimes.append(df["Time"][row])
            #print("You have already booked this room")
        
    if(fullyBooked):
        print("This room is fully booked between", fullyBookedTimes[0], "and", fullyBookedTimes[-1])
    if(alreadyBooked):
        print("You have already booked this room between", alreadyBookedTimes[0], "and", alreadyBookedTimes[-1])
            #break

def saveDf(df, name): #Lagrer df-en som en csv fil med navn = name
    df.to_csv(name)

def csvToDf(path): # lager en df på riktig format fra en csv-fil
    df = pd.read_csv(path)
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis="columns", inplace = True)
    # alt blir lest som string. Vi ønsker lister. Koden under konverterer eksempelvis ("[]" til [])
    columns = list(df.columns)
    for n in range(1, len(columns)):
        df[columns[n]] = df[columns[n]].astype(object)
        for i in range(len(df[columns[n]])):
            df[columns[n]][i] = ast.literal_eval(df[columns[n]][i]) # konverterer "[]" til [] eller "[1,2,3]" til [1,2,3]
    return df

def saveBookingData(resident, room, startTime, endTime):
    date = str(datetime.date.today())
    with open('smittesporing.txt', 'a') as smittesporing:
        smittesporing.write(date + " beboer nr " + str(resident) + " booket " + room + " fra " + startTime + " til " + endTime + "\n")


def website_booking(df, resident, room_num, start_time, end_time): # tar inn en kode på riktig format og booker tilhørende rom
    #booking_code = str(booking_code)

    resident = int(resident)
    room_num = int(room_num)
    #start_hour = booking_code[2:4]
    #start_minute = booking_code[4:6]
    #duration = int(booking_code[6:9])

    #start_time = start_time#start_hour + ":" + start_minute

    rooms = ["Bathroom", "Livingroom", "Kitchen"] # Bathroom = rom nr. 0, Livingroom = rom nr. 1, Kitchen = rom nr. 2
    maxCapacity = [1, 4, 3] # max antall personer i rommene. samme rekkefølge som over ^^
    
    room_booked = rooms[room_num]
    room_capacity = maxCapacity[room_num] # max antall personer i et rom

    booking_start_index = df.loc[df["Time"] == start_time].index[0]
    booking_end_index = df.loc[df["Time"] == end_time].index[0]
    # if(booking_start_index + int(duration / 5) < df.index[-1]):
    #     booking_end_index = booking_start_index + int(duration / 5)
    # else:
    #     booking_end_index = df.index[-1] #last index in df
    
    # håndterer feil
    fullyBooked = False
    alreadyBooked = False

    fullyBookedTimes = []
    alreadyBookedTimes = []
    

    for row in range(booking_start_index, booking_end_index): # går gjennom radene som ønskes å bookes og legger til beboeren som booker i listen over hvem som har booket rommet. (Kjører kun dersom personen ikke allerede har booket rommet)
        if((resident in df[room_booked][row]) == False): # sjekker om beboeren allerede har booket rommet
            if (len(df[room_booked][row]) < room_capacity): # sjekker om rommet har ledig kapasitet
                df[room_booked][row].append(resident)
                #print("Room booked")
            else:
                fullyBooked = True
                fullyBookedTimes.append(df["Time"][row])
                #print("This room is fully booked")

        else:
            alreadyBooked = True
            alreadyBookedTimes.append(df["Time"][row])
            #print("You have already booked this room")
    
    rooms_for_feedback = ["badet", "TV-kroken", "kjøkkenet"]

    feedback = "Du har nå booket " + rooms_for_feedback[room_num] + " fra " + start_time + " til " + end_time + "."

    if(fullyBooked):
        feedback = rooms_for_feedback[room_num].capitalize() + " er fullbooket i dette tidsrommet."
    elif(alreadyBooked):
        feedback = "Du har allerede booket " +  rooms_for_feedback[room_num] + " i dette tidsrommet."
            #break
    else:
        print("do nothing")

    return feedback