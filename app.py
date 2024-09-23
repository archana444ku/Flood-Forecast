from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import pickle
import pandas as pd
import numpy as np
import MySQLdb
import requests
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 's3cr3t_k3y'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'contact'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL connection
mysql = MySQLdb.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'],
                        password=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'])

# Load the trained model and preprocessor
model = pickle.load(open('flood_model.pkl', 'rb'))
preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))

# Weather API configurations
weather_api_key = '3c195f88f2b5332c421ae8dd55ae467e'
geolocation_api_url = 'http://ip-api.com/json/'

@app.route('/', methods=['GET', 'POST'])
def home():
    success_message = None
    error_message = None

    if request.method == 'POST':
        try:
            # Get form data
            form_data = {
                'name': request.form['name'],
                'contact': request.form['contact'],
                'datetime': request.form['datetime'],
                'destination': request.form['select1'],
                'pincode': request.form['pincode'],
                'old_aged': request.form.get('old_aged', ''),
                'mid_aged': request.form.get('mid_aged', ''),
                'children': request.form.get('children', ''),
                'message': request.form['message']
            }
            cur = mysql.cursor()
            cur.execute(
                "INSERT INTO rescue (name, contact, datetime, destination, pincode, old_aged, mid_aged, children, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                tuple(form_data.values())
            )
            mysql.commit()
            cur.close()
            success_message = "Form submitted successfully!"
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    return render_template('index.html', success_message=success_message, error_message=error_message)

@app.route('/about')
def about():
    return render_template('about.html', current_page='about')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'subject': request.form['subject'],
            'message': request.form['message']
        }
        cursor = mysql.cursor()
        cursor.execute("INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)", tuple(form_data.values()))
        mysql.commit()
        cursor.close()
        flash(f'Thank you, {form_data["name"]}! Your message has been sent successfully.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', current_page='contact')

@app.route('/services')
def services():
    return render_template('services.html', current_page='services')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html', current_page='testimonial')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            input_data = {
                'Year': int(request.form['Year']),
                'Flood_Area': request.form['Flood_Area'],
                'MonsoonIntensity': float(request.form['MonsoonIntensity']),
                'Deforestation': float(request.form['Deforestation']),
                'ClimateChange': float(request.form['ClimateChange']),
                'Siltation': float(request.form['Siltation']),
                'AgriculturalPractices': float(request.form['AgriculturalPractices']),
                'DrainageSystems': float(request.form['DrainageSystems']),
                'CoastalVulnerability': float(request.form['CoastalVulnerability']),
                'Landslides': float(request.form['Landslides']),
                'PopulationScore': float(request.form['PopulationScore']),
                'InadequatePlanning': float(request.form['InadequatePlanning']),
                'Latitude': float(request.form['Latitude']),
                'Longitude': float(request.form['Longitude'])
            }

            df_input = pd.DataFrame(input_data, index=[0])
            final_input = preprocessor.transform(df_input)
            prediction = model.predict(final_input)
            output = round(prediction[0] * 100, 2)

            cursor = mysql.cursor()
            cursor.execute("""
                INSERT INTO flood_predictions (Year, Flood_Area, MonsoonIntensity, Deforestation, ClimateChange, 
                                               Siltation, AgriculturalPractices, DrainageSystems, CoastalVulnerability, 
                                               Landslides, PopulationScore, InadequatePlanning, Latitude, Longitude, Prediction) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (*input_data.values(), output))
            mysql.commit()
            cursor.close()

            return render_template('predict.html', current_page='predict', 
                                   prediction_text=f'Predicted Flood Probability for year {input_data["Year"]}: {output}%')
        except KeyError as e:
            return f"Missing form field: {e.args[0]}", 400
        except Exception as e:
            return f"An error occurred: {str(e)}", 500
    else:
        return render_template('predict.html', current_page='predict')

@app.route('/weather_index')
def weather_index():
    return render_template('weather_index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    units = request.form.get('units', 'metric')

    if not city:
        try:
            response = requests.get(geolocation_api_url)
            location_data = response.json()
            city = location_data['city']
        except Exception as e:
            return render_template('error.html', error=str(e))
    
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units={units}'
    
    try:
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'latitude': data['coord']['lat'],
                'longitude': data['coord']['lon'],
                'temperature_unit': units
            }
            return render_template('weather.html', weather=weather_data)
        else:
            error_message = data['message']
            return render_template('error.html', error=error_message)
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query')
    params = {
        'q': query,
        'type': 'like',
        'sort': 'population',
        'cnt': 10,
        'appid': weather_api_key
    }
    response = requests.get(autocomplete_api_url, params=params)
    cities = [city['name'] for city in response.json()['list']]
    return jsonify(cities)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

# Sample data for the dashboard
data = {
    'MonsoonIntensity': [1, 2, 3, 4, 5],
    'Deforestation': [5, 3, 4, 2, 1],
    'ClimateChange': [2, 4, 1, 3, 5],
    'Siltation': [4, 2, 5, 1, 3],
    'AgriculturalPractices': [3, 5, 2, 4, 1],
    'DrainageSystems': [5, 1, 3, 2, 4],
    'CoastalVulnerability': [1, 3, 2, 5, 4],
    'Landslides': [2, 5, 1, 4, 3],
    'PopulationScore': [3, 4, 5, 1, 2],
    'InadequatePlanning': [4, 2, 3, 5, 1]
}

df = pd.DataFrame(data)

# Create a Dash app
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Define Dash app layout
dash_app.layout = html.Div([
    html.H1('Flood Prediction Dashboard'),
    dcc.Graph(
        id='flood-prediction-chart',
        figure=px.line(df, x='MonsoonIntensity', y='Deforestation', title='Flood Prediction Factors')
    )
])

if __name__ == '__main__':
    app.run(debug=True)
