# beer_app/update/views.py
from io import TextIOWrapper
import csv
from flask import render_template, url_for, request, redirect, Blueprint
from flask_login import current_user, login_required
from beer_app import db
from beer_app.models import Item, Location, Zone
from beer_app.update.forms import ItemForm, LocationForm, ZoneForm

update = Blueprint('update', __name__)

@update.route('/add_zone_form', methods=['GET', 'POST'])
@login_required
def add_zone_form():
    form = ZoneForm()

    if form.validate_on_submit():
        zone = Zone(name=form.name.data)
        db.session.add(zone)
        db.session.commit()
        return redirect(url_for('update.add_zone_form'))

    return render_template('add_zone_form.html', form=form)

@update.route('/add_zone_csv', methods=['GET', 'POST'])
@login_required
def add_zone_csv():

    if request.method == 'POST':
        csv_reader = upload_csv()
        for row in csv_reader:
            zone = Zone(name=row[1])
            db.session.add(zone)
            db.session.commit()
        return redirect(url_for('update.add_zone_form'))

    return render_template('add_zone_csv.html')

@update.route('/add_location_form', methods=['GET', 'POST'])
@login_required
def add_location_form():
    form = LocationForm()
    form.zone_id.choices = [(0,'--Select a Neighborhood--')]
    form.zone_id.choices += [
                                                (zone.id, zone.name)
                                                for zone
                                                in Zone.query.order_by('name')
                                            ]

    if form.validate_on_submit():
        location = Location(name=form.name.data,
                            address=form.address.data,
                            phone=form.address.data,
                            website=form.address.data,
                            zone_id=form.zone_id.data
                            )
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('update.add_location_form'))

    return render_template('add_location_form.html', form=form)

@update.route('/add_location_csv', methods=['GET', 'POST'])
@login_required
def add_location_csv():
    if request.method == 'POST':
        csv_reader = upload_csv()
        for row in csv_reader:
            location = Location(name=row[1],
                                address=row[2],
                                phone=row[3],
                                website=row[4],
                                zone_id=row[5]
                                )
            db.session.add(location)
            db.session.commit()
        return redirect(url_for('update.add_location_form'))
    return render_template('add_location_csv.html')

@update.route('/add_item_form', methods=['GET', 'POST'])
@login_required
def add_item_form():
    form = ItemForm()
    form.location.choices = [(0, '--Select a Brewery--')]
    form.location.choices += [
                                                (loc.id, loc.name)
                                                for loc
                                                in Location.query.order_by('name')
                                              ]

    if form.validate_on_submit():
        item = Item(location_id=form.location.data,
                    name=form.name.data,
                    style=form.style.data,
                    abv=form.abv.data,
                    ibu=form.ibu.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('update.add_item_form'))

    return render_template('add_item_form.html', form=form)

@update.route('/add_item_csv', methods=['GET','POST'])
@login_required
def add_item_csv():
    if request.method == 'POST':
        csv_reader = upload_csv()
        for row in csv_reader:
            item = Item(name=row[1],
                        style=row[2],
                        abv=row[3],
                        ibu=row[4],
                        location_id=row[5]
                        )
            db.session.add(item)
            db.session.commit()
        return redirect(url_for('update.add_item_form'))

    return render_template('add_item_csv.html')

def upload_csv():
    csv_file = request.files['file']
    csv_file = TextIOWrapper(csv_file)
    return csv.reader(csv_file, delimiter=',')
