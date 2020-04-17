from flask import render_template,url_for,flash,request,redirect,Blueprint,jsonify
from flask_login import current_user,login_required
from beer_app import db
from beer_app.models import Transaction,Zone,Location,Item
from beer_app.transactions.forms import PostTransactionForm

transactions = Blueprint('transactions', __name__)

#log a beer
@transactions.route('/post_transaction',methods=['GET','POST'])
@login_required
def post_transaction():

    form = PostTransactionForm()
    form.zone.choices = [(zone.id, zone.name) for zone in Zone.query.order_by('name')]
    form.location.choices = [(location.id, location.name) for location in Location.query.order_by('name')]
    form.item.choices=[(item.id, item.name) for item in Item.query.order_by('id')]

    if form.validate_on_submit():
        transaction = Transaction(user_id=current_user.id,
                                                item_id=form.item.data)
        db.session.add(transaction)
        db.session.commit()
        flash('Beer posted to your log!')
        return redirect(url_for('core.index'))
    
    return render_template('transactions.html',form=form)

# @transactions.route('/location/<zone>')
# def location(zone):
#     locations = Location.query.filter_by(neighborhood=zone).all()

#     location_list = []

#     for location in locations:
#         locationObj = {}
#         locationObj['id'] = location.id
#         locationObj['name'] = location.name
#         location_list.append(locationObj)

#     return jsonify({'locations' : locations_list})