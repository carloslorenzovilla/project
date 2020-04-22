# beer_app/items/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    location = SelectField('Brewery',coerce=int,validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    style = SelectField('Style',choices=[('IPA','IPA'),('Lager','Lager'),('Stout','Stout')])
    abv = StringField('ABV',validators=[DataRequired()])
    ibu = IntegerField('IBU',validators=[DataRequired()])
    submit = SubmitField('Add Beer')