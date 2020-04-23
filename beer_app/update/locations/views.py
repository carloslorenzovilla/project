# beer_app/update/locations/views.py
from flask import render_template,url_for,request,redirect,Blueprint
from flask_login import current_user,login_required
from beer_app import db
from beer_app.models import Location,Zone
from beer_app.update.locations.forms import LocationForm

locations = Blueprint('locations',__name__)

@locations.route('/add_location',methods=['GET','POST'])
@login_required
def add_location():
    form = LocationForm()
    form.zone_id.choices = [(zone.id,zone.name) for zone in Zone.query.order_by('name')]

    if form.validate_on_submit():
        location = Location(name=form.name.data,
                                        zone_id=form.zone_id.data)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('locations.add_location'))

    return render_template('location.html',form=form)
