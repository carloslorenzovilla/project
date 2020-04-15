# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from beer_app import db
from beer_app.models import User #Transaction #Recommendation
from beer_app.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from beer_app.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

# register
@users.route('/register',methods=['GET','POST'])
def register():
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)

# login

# logout

# account

# transactions

# recommendations
