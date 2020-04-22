# beer_app/items/views.py
from flask import render_template,url_for,request,redirect,Blueprint
from flask_login import current_user,login_required
from beer_app import db
from beer_app.models import Item,Location
from beer_app.items.forms import ItemForm

items = Blueprint('items',__name__)

@items.route('/add_item',methods=['GET','POST'])
@login_required
def add_item():
    form = ItemForm()
    form.location.choices = [(loc.id, loc.name) for loc in Location.query.order_by('name')]

    if form.validate_on_submit():
        item = Item(location_id=form.location.data,
                            name=form.name.data,
                            style=form.style.data,
                            abv=form.abv.data,
                            ibu=form.ibu.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('items.add_item'))

    return render_template('item.html',form=form)
