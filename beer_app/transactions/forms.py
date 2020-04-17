# transactions/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired

class PostTransactionForm(FlaskForm):
    zone = SelectField(u'Neighborhood',coerce=int,validators=[DataRequired()])
    location = SelectField(u'Brewery', coerce=int,validators=[DataRequired()])
    item = SelectField(u'Beer', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Post')

