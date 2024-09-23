# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired

class WeatherForecasterForm(FlaskForm):
    area = StringField('Area', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Submit')
