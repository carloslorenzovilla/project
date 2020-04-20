from flask import render_template,url_for,flash,request,redirect,Blueprint
from flask_login import current_user,login_required
from beer_app import db
from beer_app.models import Zone
from beer_app.zones.forms import ZoneForm

zones = Blueprint('zones',__name__)

@zones.route('/add_zone',methods=['GET','POST'])
@login_required
def add_zone():
    form = ZoneForm()

    if form.validate_on_submit():
        zone = Zone(name=form.name.data)
        db.session.add(zone)
        db.session.commit()
        return redirect(url_for('zones.add_zone'))

    return render_template('zone.html', form=form)