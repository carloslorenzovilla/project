# beer_app/init.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_s3 import FlaskS3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password3X'

app.config['FLASKS3_BUCKET_NAME'] = 'beerappfiles'
s3 = FlaskS3(app)

########################
#### DATABASE SETUP ####
########################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

######################
#### LOGIN CONFIG ####
######################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

####################
#### BLUEPRINTS ####
####################

from beer_app.core.views import core
from beer_app.update.views import update
from beer_app.users.views import users
from beer_app.actions.views import actions
from beer_app.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(update)
app.register_blueprint(users)
app.register_blueprint(actions)
app.register_blueprint(error_pages)
