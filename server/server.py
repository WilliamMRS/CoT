# Imports
from flask import Flask, url_for, request, render_template
from markupsafe import escape
# Private modules
import cot
import weather
import json
import booking_functions
import key
import pandas as pd
import csv
import numpy as np

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
        response = app.response_class(
            response=json.dumps(weather.liveForecast().__dict__, indent=4, sort_keys=True, default=str),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return "POST Not ready yet"

@app.route('/api/bookRoom', methods=['POST', 'GET'])
def bookRoom():
    if request.method == 'POST':
        print(request.form)
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

        return render_template('booking.html', feedback=feedback)
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
    cachedData = [0,[],[],[],[],[],[]] # where index 0 is empty, 1-6 is userdata in form of 
    startKey = "startTime"
    
    # TODO: Account for multiple bookings. This method only accounts for one booking in a 24 hour span.
    for index, row in df.iterrows():
        print(index)
        # ID's: 1-6
        if len(row[1]):
            for userid in row[1]: # userID's that have booked this room at this time.
                for booking in cachedData[userid]:  # if this userID's been already checked for this time, skip it.
                    startTime = booking["startTime"].split(":")
                    startTime = int(startTime[0]*60) + startTime[1]
                    print(startTime)

                cachedData[userid] = {
                    'startTime': row[0],
                    'endTime': 0,
                    'room': 'Bad'
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
    df = pd.read_csv('../strøm_&_simulering/powerUsage.csv')
    # Extract solar panel power generation
    # Extract total power generated

    # ganger strømforbrukslisten med prisen av strøm for å plotte kostnaden til brukt strøm.
    costOfPower = (df.iloc[:, [14]]).to_numpy().tolist() # powerUsage
    for i in range (0, len(costOfPower)):
        cost = (df.iloc[:, [15]]).to_numpy().tolist()[i][0]
        usage = (costOfPower[i][0])
        costOfPower[i][0] = usage * cost

    data = {
        "powerUsage": (df.iloc[:, [14]]).to_numpy().tolist(),
        "solarSavings": (df.iloc[:, [17]]).to_numpy().tolist(),
        "PvGeneration": (df.iloc[:, [16]]).to_numpy().tolist(),
        "costOfPower": costOfPower,
        "time": (df.iloc[:, [0]]).to_numpy().tolist(),
    }
    response = app.response_class(
        response=json.dumps(data, indent=4, sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )
    # return as object of three lists, one with usage, one with generation and one with timestamps.
    return response

@app.route('/api/getOccupants', methods=['GET'])
def getOccupants():
    data = []
    with open('../strøm_&_simulering/user_locations.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    response = app.response_class(
        response=json.dumps(data, indent=4, sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )

    # return as object of three lists, one with usage, one with generation and one with timestamps.
    return response


# TODO: Implement powerusage api and read/write to csv

# TODO: Implement feedback. stop redirect. When booking

# TODO: LIVE CHARTS:
# https://nagix.github.io/chartjs-plugin-streaming/
# https://www.chartjs.org/docs/latest/developers/updates.html
# https://www.chartjs.org/docs/latest/charts/line.html