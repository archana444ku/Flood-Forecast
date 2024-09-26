from flask import Flask, render_template, request, flash, redirect, url_for  # Importing necessary modules from Flask for web routing, rendering templates, and handling requests
import pickle  # Importing pickle for loading the saved machine learning model and preprocessor
# import numpy as np  # Importing numpy for numerical operations (though not used in this snippet, it's commonly used for data handling)
import pandas as pd  # Importing pandas for data manipulation and analysis
from flask_wtf import FlaskForm  # Importing FlaskForm from Flask-WTF for form handling
from wtforms import StringField, SubmitField  # Importing form fields from WTForms for creating web forms
from wtforms.validators import DataRequired  # Importing DataRequired validator to ensure form fields are not empty

import requests
from flask import Flask, render_template, request, jsonify
# import MySQLdb
# import mysql.connector

from flask import Flask, render_template
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Flask(__name__)  # Creating a new Flask web application instance
# Set the secret key for CSRF protection to secure form submissions and prevent cross-site request forgery
app.config['SECRET_KEY'] = 's3cr3t_k3y'


# For weather fore cast 
weather_api_key = '3c195f88f2b5332c421ae8dd55ae467e'
autocomplete_api_url = 'http://api.openweathermap.org/data/2.5/find'
geolocation_api_url = 'http://ip-api.com/json/'


# # MySQL configurations
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'contact'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
# mysql = MySQLdb.connect(host=app.config['MYSQL_HOST'],
#                         user=app.config['MYSQL_USER'],
#                         password=app.config['MYSQL_PASSWORD'],
#                         db=app.config['MYSQL_DB'])

# Load the trained machine learning model and preprocessor from pickle files
model = pickle.load(open('flood_model.pkl', 'rb'))  # Loading the RandomForestRegressor model
preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))  # Loading the preprocessor used for feature scaling and encoding

@app.route('/', methods=['GET', 'POST'])
def home():
    success_message = None
    error_message = None

    if request.method == 'POST':
        try:
            # Get form data
            name = request.form['name']
            contact = request.form['contact']
            datetime = request.form['datetime']
            destination = request.form['select1']
            pincode = request.form['pincode']
            old_aged = request.form.get('old_aged', '')
            mid_aged = request.form.get('mid_aged', '')
            children = request.form.get('children', '')
            message = request.form['message']

            # Create a cursor to execute queries
            cur = mysql.cursor()

            # Insert data into MySQL
            cur.execute(
                "INSERT INTO rescue (name, contact, datetime, destination, pincode, old_aged, mid_aged, children, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (name, contact, datetime, destination, pincode, old_aged, mid_aged, children, message)
            )

            # Commit to the database
            mysql.commit()

            # Close the connection
            cur.close()

            # Set success message
            success_message = "Form submitted successfully!"
        except Exception as e:
            # Set error message
            error_message = f"An error occurred: {str(e)}"

    return render_template('index.html', success_message=success_message, error_message=error_message)
 

@app.route('/about')
def about():
    # Route for the about page
    return render_template('about.html', current_page='about')  # Rendering the about page template with a variable indicating the current page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Insert data into MySQL
        cursor = mysql.cursor()
        cursor.execute("INSERT INTO contacts(name, email, subject, message) VALUES (%s, %s, %s, %s)", (name, email, subject, message))
        mysql.commit()
        cursor.close()

        flash(f'Thank you, {name}! Your message has been sent successfully.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', current_page='contact')  # Rendering the contact page template with a variable indicating the current page

@app.route('/services')
def services():
    # Route for the services page
    return render_template('services.html', current_page='services')  # Rendering the services page template with a variable indicating the current page

@app.route('/testimonial')
def testimonial():
    # Route for the testimonial page
    return render_template('testimonial.html', current_page='testimonial')  # Rendering the testimonial page template with a variable indicating the current page



# This is predict model code 
# Start code here


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Extracting input data from the form
            year = int(request.form['Year'])
            flood_area = request.form['Flood_Area']
            monsoon_intensity = float(request.form['MonsoonIntensity'])
            deforestation = float(request.form['Deforestation'])
            climate_change = float(request.form['ClimateChange'])
            siltation = float(request.form['Siltation'])
            agricultural_practices = float(request.form['AgriculturalPractices'])
            drainage_systems = float(request.form['DrainageSystems'])
            coastal_vulnerability = float(request.form['CoastalVulnerability'])
            landslides = float(request.form['Landslides'])
            population_score = float(request.form['PopulationScore'])
            inadequate_planning = float(request.form['InadequatePlanning'])
            Latitude = float(request.form['Latitude'])
            Longitude = float(request.form['Longitude'])
             
            # Convert the data to a dictionary
            data = {
                'Year': [year],
                'Flood_Area': [flood_area],
                'MonsoonIntensity': [monsoon_intensity],
                'Deforestation': [deforestation],
                'ClimateChange': [climate_change],
                'Siltation': [siltation],
                'AgriculturalPractices': [agricultural_practices],
                'DrainageSystems': [drainage_systems],
                'CoastalVulnerability': [coastal_vulnerability],
                'Landslides': [landslides],
                'PopulationScore': [population_score],
                'InadequatePlanning': [inadequate_planning],
                'Latitude': [Latitude],
                'Longitude': [Longitude]
            }

            # Convert the data to a DataFrame
            df_input = pd.DataFrame(data)

            # Preprocess the input data
            final_input = preprocessor.transform(df_input)

            # Make prediction
            prediction = model.predict(final_input)

            # Convert prediction to percentage
            output = round(prediction[0] * 100, 2)

            # Insert into the database
            # cursor = mysql.cursor()
            # sql_query = """
            # INSERT INTO flood_predictions (Year, Flood_Area, MonsoonIntensity, Deforestation, ClimateChange, Siltation,
            #                                AgriculturalPractices, DrainageSystems, CoastalVulnerability, Landslides,
            #                                PopulationScore, InadequatePlanning, Latitude, Longitude, Prediction) 
            # VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            # """
            # cursor.execute(sql_query, (year, flood_area, monsoon_intensity, deforestation, climate_change, siltation,
            #                            agricultural_practices, drainage_systems, coastal_vulnerability, landslides,
            #                            population_score, inadequate_planning, Latitude, Longitude, output))
            # mysql.commit()
            # cursor.close()

            return render_template('predict.html', current_page='predict', 
                                   prediction_text=f'Predicted Flood Probability for year {year}: {output}%')
        except KeyError as e:
            return f"Missing form field: {e.args[0]}", 400
        except Exception as e:
            return f"An error occurred: {str(e)}", 500
    else:
        return render_template('predict.html', current_page='predict')


# End code here model predic 






# for wether forecast new
#start code
@app.route('/weather_index')
def weather_index():
    return render_template('weather_index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    units = request.form.get('units', 'metric')  # Default to metric units (Celsius)
    
    if not city:  # If city is not provided, attempt to get user's location
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

#start end code of weather forecost



# This is old forecaster code 
# start code
@app.route('/forecaster', methods=['GET', 'POST'])
def forecaster():
    # Route for the forecaster page, handling both GET and POST requests
    form = MyForm()  # Create an instance of the form class MyForm

    if form.validate_on_submit():  # Check if the form is submitted and validated successfully
        flash('Form successfully submitted!', 'success')  # Display a flash message indicating successful form submission
        return redirect(url_for('forecaster'))  # Redirect to the forecaster page after form submission
    
    # Render the forecaster page with the form object for GET requests (initial page load)
    return render_template('forecaster.html', form=form)

class MyForm(FlaskForm):
    # Define a form class using Flask-WTF
    area = StringField('Area', validators=[DataRequired()])  # Define a field for Area with a DataRequired validator
    latitude = StringField('Latitude', validators=[DataRequired()])  # Define a field for Latitude with a DataRequired validator
    longitude = StringField('Longitude', validators=[DataRequired()])  # Define a field for Longitude with a DataRequired validator
    submit = SubmitField('Get Weather')  # Define a submit button for the form

# end code of forecaster





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

# Define custom CSS styles
styles = {
    'container': {
        'display': 'flex',
        'flex-direction': 'row',
        'justify-content': 'space-between',
        'width': '80%',
        'margin': '0 auto',
        'font-family': 'Arial, sans-serif'
    },
    'header': {
        'textAlign': 'center',
        'padding': '10px',
        'background-color': '#4CAF50',
        'color': 'white',
        'font-size': '18px',
        'border-radius': '5px',
        'margin-bottom': '20px',
        'width': '50%',
        'margin': '0 auto'
    },
    'controls': {
        'width': '30%',
        'padding': '10px',
        'border': '1px solid #ddd',
        'border-radius': '5px',
        'margin-right': '20px',
        'background-color': '#f9f9f9'
    },
    'graph': {
        'width': '65%',
        'border': '1px solid #ddd',
        'border-radius': '5px',
        'padding': '10px',
        'background-color': '#ffffff'
    }
}

# Dash app layout
dash_app.layout = html.Div([
    html.Div("Weather Forecast Analysis Dashboard", style=styles['header']),
    html.Div(style=styles['container'], children=[
        html.Div(style=styles['controls'], children=[
            html.Label("Select X-axis:"),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns],
                value='MonsoonIntensity',
                clearable=False
            ),
            html.Label("Select Y-axis:"),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns],
                value='Deforestation',
                clearable=False
            ),
            html.Label("Select Chart Type:"),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Scatter Plot', 'value': 'scatter'}
                ],
                value='line',
                clearable=False
            )
        ]),
        html.Div(dcc.Graph(id='chart'), style=styles['graph'])
    ])
])

# Callback to update graph
@dash_app.callback(
    Output('chart', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('chart-type-dropdown', 'value')]
)
def update_graph(x_axis, y_axis, chart_type):
    if chart_type == 'line':
        fig = px.line(df, x=x_axis, y=y_axis,
                      labels={'x': x_axis, 'y': y_axis},
                      title=f'Line Chart of {x_axis} vs {y_axis}')
    elif chart_type == 'bar':
        fig = px.bar(df, x=x_axis, y=y_axis,
                     labels={'x': x_axis, 'y': y_axis},
                     title=f'Bar Chart of {x_axis} vs {y_axis}')
    elif chart_type == 'scatter':
        fig = px.scatter(df, x=x_axis, y=y_axis,
                         labels={'x': x_axis, 'y': y_axis},
                         title=f'Scatter Plot of {x_axis} vs {y_axis}')
    return fig

# Flask route to render the dashboard.html template
@app.route('/dashboard',endpoint='dashboard_page', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode to enable debugging features
