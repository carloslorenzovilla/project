from flask import render_template,url_for,flash,request,redirect,Blueprint
from flask_login import current_user,login_required
from beer_app import db
from beer_app.models import Location
from beer_app.locations.forms import LocationForm

locations = Blueprint('locations',__name__)

@locations.route('/add_location',methods=['GET','POST'])
@login_required
def add_location():
    form = LocationForm()

    if form.validate_on_submit():
        location = Location(name=form.name.data,
                                        zone_id=form.zone_id.data)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('locations.add_location'))

    return render_template('location.html',form=form)