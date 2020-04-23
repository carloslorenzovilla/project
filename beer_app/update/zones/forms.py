from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class ZoneForm(FlaskForm):
    name = StringField('Neighborhood',validators=[DataRequired()])
    submit = SubmitField('Add Neighborhood')