# Imports
from flask import Flask, url_for, request, render_template
from markupsafe import escape
# Private modules
import cot
import weatherData
import json
import booking_functions
import key

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

@app.route('/api/bookRoom', methods=['POST', 'GET'])
def bookRoom():
    if request.method == 'POST':
        print("GETTING FORM!")
        print(request.form.get("room_form"))
        print(request.form.get("time_start"))
        print(request.form.get("time_end"))
        print(request.form.get("user_name"))
        return render_template('dashboard.html')
    else:
        return render_template('dashboard.html')
# TODO: Implement powerusage api and read/write to csv

# TODO: Implement booking system with CoT and a storage (csv file) for all bookings.

# TODO: LIVE CHARTS:
# https://nagix.github.io/chartjs-plugin-streaming/
# https://www.chartjs.org/docs/latest/developers/updates.html
# https://www.chartjs.org/docs/latest/charts/line.html