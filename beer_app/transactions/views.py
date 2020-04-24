# beer_app/transactions/views.py
from flask import render_template, url_for, request, redirect, Blueprint, jsonify
from flask_login import current_user, login_required
from beer_app import db
from beer_app.models import Log, Rec, Zone, Location, Item
from beer_app.transactions.forms import PostLogForm
#from beer_app.rec_eng.generate import generate_rec

transactions = Blueprint('transactions', __name__)

# log a beer
@transactions.route('/log_item', methods=['GET', 'POST'])
@login_required
def log_item():

    form = PostLogForm()
    form.zone.choices = [(zone.id, zone.name)
                         for zone
                         in Zone.query.order_by('name')]
    form.loc.choices = [(loc.id, loc.name)
                        for loc
                        in Location.query.order_by('name')]
    form.item.choices = [(item.id, item.name)
                         for item
                         in Item.query.order_by('location_id')]

    if form.validate_on_submit():
        transaction = Log(user_id=current_user.id,
                          item_id=form.item.data)
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transactions.log_item'))

    page = request.args.get('page',1,type=int)
    user_post_log = Log.query.filter_by(user_id=current_user.id).order_by(Log.date.desc()).paginate(page=page,per_page=3)

    return render_template('log_item.html',form=form,user_post_log=user_post_log)

# get recommendation
@transactions.route('/get_rec', methods=['GET', 'POST'])
@login_required
def get_rec():

    form = PostLogForm()
    form.zone.choices = [(zone.id, zone.name)
                         for zone
                         in Zone.query.order_by('name')]
    form.loc.choices = [(loc.id, loc.name)
                        for loc
                        in Location.query.order_by('name')]

    if form.validate_on_submit():
        # get_rec = generate_rec(user_id=current_user.id,
        #                                zone_id=form.zone_id.data,
        #                                location_id=form.location_id.data)
        #
        # rec will then return a list of three recommendations
        #
        # recs = Recs(user_id = current_user.id,
        #                                            item_id = get_rec.list)
        #
        # db.session.add(recs)
        # db.session.commit()
        return redirect(url_for('transactions.get_rec'))

    page = request.args.get('page', 1, type=int)
    user_recs = Rec.query.filter_by(user_id=current_user.id).order_by(
        Rec.date.desc()).paginate(page=page, per_page=3)

    return render_template('rec.html', form=form, user_recs=user_recs)


@transactions.route('/loc/<zone>')
def location(zone):

    location_list = [{'id': location.id, 'name': location.name}
                     for location
                     in Location.query.filter_by(zone_id=zone).all()]

    return jsonify({'locs': location_list})


@transactions.route('/item/<loc>')
def item(loc):

    item_list = [{'id': item.id, 'name': item.name}
                 for item
                 in Item.query.filter_by(location_id=loc).all()]

    return jsonify({'items': item_list})
