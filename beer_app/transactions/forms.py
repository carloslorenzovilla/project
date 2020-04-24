# beer_app/transactions/forms.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class PostLogForm(FlaskForm):
    zone = SelectField('Neighborhood', coerce=int, validators=[DataRequired()])
    loc = SelectField('Brewery', coerce=int, validators=[DataRequired()])
    item = SelectField('Beer', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Get Rec!')
