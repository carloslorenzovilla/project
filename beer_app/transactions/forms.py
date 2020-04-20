# transactions/forms.py
from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectField
from wtforms.validators import DataRequired

class PostTransactionForm(FlaskForm):
    zone = SelectField('Neighborhood',coerce=int,validators=[DataRequired()])
    location = SelectField('Brewery',coerce=int)
    item = SelectField('Beer', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Post')

