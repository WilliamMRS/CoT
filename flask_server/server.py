# Imports
from flask import Flask, url_for, request, render_template
from markupsafe import escape
# Private modules
import cot
import weatherData
import json
import booking_functions
import key
import pandas as pd

app = Flask(__name__, static_url_path='/static')

token = key.token

cot_api = cot.cot_api(token) # grab the api and pass it the token value

print(cot_api.get_data("1429"))

# load static files
#{{ url_for('static', filename='dashboard.css') }}

# Routing - Visible public sites
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# API - Data for the dashboard

# Routing - Secured API
@app.route('/api/forecast', methods=['GET', 'POST'])
def forecast():
    if request.method == 'GET':
        print(weatherData.Get_data_now())
        #response = app.response_class(
        #    response=json.dumps(weatherData.Get_data_now().__dict__, indent=4, sort_keys=True, default=str),
        #    status=200,
        #    mimetype='application/json'
        #)
        return 0 #response
    else:
        return "POST Not ready yet"

@app.route('/lol')
def responsefunc():
    return 'lmao'

@app.route('/api/bookRoom', methods=['POST', 'GET'])
def bookRoom():
    if request.method == 'POST':
        room_id = request.form.get("room_form") #roomid 0: bad, 1: stue/tvkrok, 2: kjøkken
        start_time = request.form.get("time_start") # 14:30
        end_time = request.form.get("time_end") # 15:30
        resident_id = request.form.get("user_name") #userid: 1: william, 2: fredrik, 3: Jens, 4: Bendik, 5: Erling, 6: Julenissen

        # Sjekk om tiden er ledig i CSV filen
        # Hvis ledig, book, hvis ikke, redirect til '
        df = booking_functions.csvToDf("booking.csv")
        booking_functions.updateTime(df)
        feedback = booking_functions.website_booking(df, resident_id, room_id, start_time, end_time)
        booking_functions.saveDf(df, "booking.csv")
        booking_functions.saveBookingData(resident_id, room_id, start_time, end_time)
        print(feedback)
        print(df)

        return render_template('dashboard.html')
    else:
        return render_template('dashboard.html')

def returnUserIds(userList):
    for ids in userList:
        print(ids)
    return 0


# TODO: show current bookings as a list in the dashboard
@app.route('/api/getBookings', methods=['POST', 'GET'])
def readRooms():
    bookings = { "data": [] }
    df = booking_functions.csvToDf("booking.csv")
    booking_functions.updateTime(df)
    print(df)

    # read dataframe for bookings and add them to bookings{} as a list of all registered bookings.
    # Store id of a user, and start time. Also store endtime using 'previous time' variable.
    cachedData = [0,{},{},{},{},{},{}] # where index 0 is empty, 1-6 is userdata in form of 
    startKey = "startTime"
    # {
    #   startTime: "",
    #   lastTime: ""   //This means last stored time
    # }
    
    # TODO: Account for multiple bookings. This method only accounts for one booking in a 24 hour span.

    for index, row in df.iterrows():
        print(index)
        # ID's: 1-6
        if len(row[1]):
            for userid in row[1]:
                if startKey in cachedData[userid]:
                    cachedData[userid]['lastTime'] =  row[0]
                else:
                    cachedData[userid] = {
                        'startTime': row[0],
                        'room': 'Bad'
                    }
        if len(row[2]):
            for userid in row[2]:
                if startKey in cachedData[userid]:
                    cachedData[userid]['lastTime'] =  row[0]
                else:
                    cachedData[userid] = {
                        'startTime': row[0],
                        'room': 'Stue'
                    }
        if len(row[3]):
            for userid in row[3]:
                if startKey in cachedData[userid]:
                    cachedData[userid]['lastTime'] = row[0]
                else:
                    cachedData[userid] = {
                        'startTime': row[0],
                        'room': 'Kjøkken'
                    }

    print(cachedData)

    response = app.response_class(
        response=json.dumps(bookings, indent=4, sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/getPowerUsage', methods=['GET'])
def getPowerUsage():
    return {}

# TODO: Implement powerusage api and read/write to csv

# TODO: Implement feedback. stop redirect. When booking

# TODO: LIVE CHARTS:
# https://nagix.github.io/chartjs-plugin-streaming/
# https://www.chartjs.org/docs/latest/developers/updates.html
# https://www.chartjs.org/docs/latest/charts/line.html