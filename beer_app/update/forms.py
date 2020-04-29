# beer_app/update/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired

class ZoneForm(FlaskForm):
    name = StringField('Neighborhood',validators=[DataRequired()])
    submit = SubmitField('Add Neighborhood')

class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Street Address, City, State ZIP')
    phone = StringField('Phone')
    website = StringField('Website')
    zone_id = SelectField('Neighborhood ID', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Brewery')

class ItemForm(FlaskForm):
    location = SelectField('Brewery', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    style = SelectField('Style',choices=[('IPA','IPA'),('Lager','Lager'),('Stout','Stout')])
    abv = StringField('ABV')
    ibu = IntegerField('IBU')
    submit = SubmitField('Add Beer')
