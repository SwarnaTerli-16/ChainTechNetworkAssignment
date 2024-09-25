from flask import Flask, render_template, request, redirect
import datetime
import requests
import os

app = Flask(__name__)

# API key
API_KEY = '0010ff61578879920f95338224a9f16c'


cities = ['Visakhapatnam', 'India', 'US', 'New York', 'London', 'China', 'Tokyo', 'Sydney', 'Paris', 'Berlin', 'Dubai']

# File path for storing submissions (Exercise 5)
SUBMISSION_FILE = 'submissions.txt'

# Function to get weather data for a city
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if data['cod'] == 200:
        weather = {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }
        return weather
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    # Get current date and time
    now = datetime.datetime.now()
    date = now.strftime("%A, %d %B %Y")
    time = now.strftime("%H:%M:%S")
    
    weather = None
    selected_city = 'Visakhapatnam'  # Default city

    if request.method == 'POST' and 'city' in request.form:
        selected_city = request.form['city']
        weather = get_weather(selected_city)

    if not weather:
        weather = get_weather(selected_city)

    return render_template('index.html', date=date, time=time, weather=weather, cities=cities, selected_city=selected_city)

# Exercise 4: Form handling
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    # Store the form data in a file (Exercise 5)
    with open(SUBMISSION_FILE, 'a') as file:
        file.write(f"Name: {name}, Email: {email}\n")
    
    return redirect('/submissions')

# Exercise 5: Data Persistence - View submissions
@app.route('/submissions', methods=['GET'])
def submissions():
    if os.path.exists(SUBMISSION_FILE):
        with open(SUBMISSION_FILE, 'r') as file:
            submissions = file.readlines()
    else:
        submissions = []

    return render_template('submissions.html', submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True)
