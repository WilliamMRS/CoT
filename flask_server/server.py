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
def login():
    if request.method == 'GET':
        response = app.response_class(
            response=json.dumps(weatherData.Get_data_now().__dict__, indent=4, sort_keys=True, default=str),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return "POST Not ready yet"

@app.route('/lol')
def responsefunc():
    return 'lmao'

@app.route('/api/bookRoom', methods=['POST', 'GET'])
def bookRoom():
    if request.method == 'POST':
        print("GETTING FORM!")
        print(request.form.get("room_form")) #roomid 0: bad, 1: stue/tvkrok, 2: kjøkken
        print(request.form.get("time_start")) # 14:30
        print(request.form.get("time_end")) # 15:30
        print(request.form.get("user_name")) #userid: 1: william, 2: fredrik, 3: Jens, 4: Bendik, 5: Erling, 6: Julenissen

        roomName = request.form.get("room_form")

        # Sjekk om tiden er ledig i CSV filen
        # Hvis ledig, book, hvis ikke, redirect til '

        return render_template('dashboard.html')
    else:
        return render_template('dashboard.html')

# TODO: show current bookings as a list in the dashboard
@app.route('/api/getBookings', methods=['POST', 'GET'])
def readRooms():
    bookings = { "data": [] }
    df = booking_functions.csvToDf("booking.csv")
    print(df)

    # read dataframe for bookings and add them to bookings{} as a list
    for index, row in df.iterrows():
        print(row[0], row[1])

    response = app.response_class(
        response=json.dumps(bookings.Get_data_now().__dict__, indent=4, sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )
    return response

# TODO: Implement powerusage api and read/write to csv

# TODO: LIVE CHARTS:
# https://nagix.github.io/chartjs-plugin-streaming/
# https://www.chartjs.org/docs/latest/developers/updates.html
# https://www.chartjs.org/docs/latest/charts/line.html