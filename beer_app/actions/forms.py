# beer_app/actions/forms.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class RecActionForm(FlaskForm):
    zone = SelectField('Neighborhood', 
                                    coerce=int, 
                                    choices=[(0,' --Select a Neighborhood--')])
    loc=SelectField('Brewery', 
                                    coerce=int, 
                                    choices=[(0, '--Select a Brewery--')])
    submit = SubmitField('Submit!')

class LogActionForm(RecActionForm):
    item = SelectField('Beer', 
                                    coerce=int, 
                                    validators=[DataRequired()],
                                    choices=[(0, '--Select a Beer--')])
