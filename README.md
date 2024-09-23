# flood_forecaster

This project aims to predict flood probability based on various environmental and geographical factors, and also assist in forecasting weather conditions and identifying nearby rescue teams. The system allows users to input key parameters such as **Year**, **Flood Area**, **Monsoon Intensity**, **Deforestation**, **Climate Change**, **Siltation**, **Agricultural Practices**, **Drainage Systems**, **Coastal Vulnerability**, **Landslides**, **Population Score**, **Inadequate Planning**, **Latitude**, and **Longitude**, and provides a flood probability prediction for a given year.

## Key Features

- **Flood Prediction:** Users input values for multiple factors (scaled between 1 to 10), and the system predicts the likelihood of a flood.
- **Weather Forecaster:** Provides weather forecasts for selected areas.
- **Rescue Prediction:** Identifies nearby rescue teams and stores contact information in the database for emergency response.
- **Dashboard:** Displays data and predictions for quick overview and analysis.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Flask
- **Database:** MySQL
- **Machine Learning:** Model built using Jupyter Notebook with CSV data
- **Libraries:** `scikit-learn`, `pandas`, `numpy`, and others (see [requirements](#requirements))
  
## How It Works

1. Users fill in key flood-related parameters on the prediction form.
2. The system processes the input and returns a **Predicted Flood Probability** for a given year, e.g., "Predicted Flood Probability for year 2021: 62.24%."
3. A dashboard displays real-time data, rescue contacts, and forecast summaries.
4. Users can also view and forecast weather patterns using the weather forecaster page.
  
## Installation Guide

To run this project locally, follow the steps below:

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- MySQL
- Flask
- Jupyter Notebook (for training the machine learning model)

1. **Prerequisites**
Python 3.8 or higher: Make sure you have Python installed on your system.
MySQL: You need a MySQL database to store the project's data.
Virtual Environment: It's recommended to use a virtual environment to isolate project dependencies.
Installation

### Steps

1. **Clone the Repository:**


git clone https://github.com/your-username/flood-forecasting-system.git  
Navigate to the project directory:

cd flood-forecasting-system  
Create a virtual environment (using venv):

python -m venv venv  
Activate the virtual environment:

Linux/macOS:
source venv/bin/activate  
Windows:
venv\Scripts\activate  
Install required packages:

pip install -r requirements.txt  
Set up the database:

Create a new MySQL database named flood_forecasting.
Configure the database connection details in the config.py file.
Run the Flask application:

flask run  
Access the application:
Open your web browser and go to http://127.0.0.1:5000/.

Usage
The application provides the following features:

Flood Predictor:
Enter data for different parameters (e.g., rainfall, river levels, soil saturation) using a scale of 1 to 10.
Submit the form to view a flood probability prediction for a given year.
Weather Forecaster:
Provides real-time weather updates for the area.
Rescue Team Contact:
Displays contact information for nearby rescue teams based on predicted data.
Requirements
The project utilizes the following libraries and packages:

absl-py
altair
Flask
Flask-SQLAlchemy
scikit-learn
pandas
numpy
matplotlib
jupyter
mysqlclient
... (other dependencies listed in requirements.txt)

