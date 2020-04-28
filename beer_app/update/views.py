# beer_app/update/views.py
from flask import render_template,url_for,request,redirect,Blueprint
from flask_login import current_user,login_required
from beer_app import db
from beer_app.models import Item,Location,Zone
from beer_app.update.forms import ItemForm,LocationForm,ZoneForm

update = Blueprint('update', __name__)

@update.route('/add_zone', methods=['GET', 'POST'])
@login_required
def add_zone():
    form = ZoneForm()

    if form.validate_on_submit():
        zone = Zone(name=form.name.data)
        db.session.add(zone)
        db.session.commit()
        return redirect(url_for('update.add_zone'))

    return render_template('zone.html', form=form)

locations = Blueprint('locations',__name__)

@update.route('/add_location',methods=['GET','POST'])
@login_required
def add_location():
    form = LocationForm()
    form.zone_id.choices = [(zone.id,zone.name) for zone in Zone.query.order_by('name')]

    if form.validate_on_submit():
        location = Location(name=form.name.data,
                                        zone_id=form.zone_id.data)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('update.add_location'))

    return render_template('location.html',form=form)

items = Blueprint('items', __name__)

@update.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
    form.location.choices = [(loc.id, loc.name)
                             for loc in Location.query.order_by('name')]

    if form.validate_on_submit():
        item = Item(location_id=form.location.data,
                    name=form.name.data,
                    style=form.style.data,
                    abv=form.abv.data,
                    ibu=form.ibu.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('update.add_item'))

    return render_template('item.html', form=form)


