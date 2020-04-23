# beer_app/update/locations/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired

class LocationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    zone_id = SelectField('Neighborhood ID',coerce=int,validators=[DataRequired()])
    submit = SubmitField('Add Brewery')

    