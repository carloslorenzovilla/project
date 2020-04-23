# beer_app/transactions/views.py
from flask import render_template,url_for,request,redirect,Blueprint,jsonify
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
    form.zone.choices = [(zone.id, zone.name) 
                                        for zone 
                                        in Zone.query.order_by('name')]
    form.loc.choices = [(loc.id, loc.name) 
                                        for loc 
                                        in Location.query.order_by('name')]
    form.item.choices=[(item.id, item.name) 
                                        for item 
                                        in Item.query.order_by('location_id')]

    if form.validate_on_submit():
        transaction = Transaction(user_id=current_user.id,
                                                item_id=form.item.data)
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transactions.post_transaction'))
    
    return render_template('transactions.html',form=form)

#get recommendation
@transactions.route('/get_recommendation',methods=['GET','POST'])
@login_required
def get_recommendation():
    
    form = PostTransactionForm()
    form.zone.choices = [(zone.id, zone.name)
                         for zone
                         in Zone.query.order_by('name')]
    form.loc.choices = [(loc.id, loc.name)
                        for loc
                        in Location.query.order_by('name')]

    if form.validate_on_submit():
        return redirect(url_for('transactions.get_recommendation'))

    return render_template('recommendations.html',form=form)

@transactions.route('/loc/<zone>')
def location(zone):

    location_list = [{'id':location.id,'name':location.name} 
                                for location 
                                in Location.query.filter_by(zone_id=zone).all()]

    return jsonify({'locs' : location_list})

@transactions.route('/item/<loc>')
def item(loc):

    item_list = [{'id': item.id, 'name': item.name} 
                        for item 
                        in Item.query.filter_by(location_id=loc).all()]

    return jsonify({'items' : item_list})
