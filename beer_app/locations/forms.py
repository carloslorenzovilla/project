# beer_app/locations/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from wtforms.validators import DataRequired

class LocationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    zone_id = IntegerField('Neighborhood ID',validators=[DataRequired()])
    submit = SubmitField('Add Brewery')

    