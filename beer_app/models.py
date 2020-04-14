from beer_app import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

#Allows the use of "is user authenticated" functionality in templates
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# USER ACCOUNT
class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    transactions = db.relationship('Transaction',backref='user',lazy='dynamic')
    recs = db.relationship('Recommendation',backref='user',lazy='dynamic')

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username: {self.username} Email: {self.email}"

# BEER LOGS
class Transaction(db.Model):

    __tablename__ = 'transactions'

    users = db.relationship(User)
    items = db.relationship(Item)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    item_id = db.Column(db.Integer,db.ForeignKey('items.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __init__(self,user_id,item_id):
        self.user_id = user_id
        self.item_id = item_id

    def __repr__(self):
        return f"Transaction #{self.id} -- Beer ID: {self.item_id} -- User ID: {self.user_id}"

# RECOMMENDATIONS
class Recommendation(db.Model):

    __tablename__ = 'recommendations'

    users = db.relationship(User)
    items = db.relationship(Item)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    item_id = db.Column(db.Integer,db.ForeignKey('items.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __init__(self,user_id,item_id):
        self.user_id = user_id
        self.item_id = item_id

    def __repr__(self):
        return f"Rec ID: {self.id} -- Beer ID: {self.item_id} -- User ID: {self.user_id}"

# BEERS
class Item(db.Model):

    __tablename__ = 'items'

    locations = db.relationship(Location)

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False,index=True)
    style = db.Column(db.String(64),nullable=False,index=True)
    abv = db.Column(db.Decimal(3,1),nullable=False,index=True)
    ibu = db.Column(db.Integer(3),index=True)
    location_id = db.Column(db.Integer,db.ForeignKey('locations.id'),nullable=False)

    def __init__(self,name,style,abv,ibu=None,location_id):
        self.name = name
        self.style = style
        self.abv = abv
        self.ibu = ibu
        self.location_id = location_id

    def __repr__(self):
        return f"{self.name} -- {self.locations.name} -- ABV: {self.abv} -- IBU: {self.ibu}"

# BREWERIES   
class Location(db.Model):

    __tablename__ = 'locations'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False,index=True)
    address = db.Column(db.String(64),nullable=False,index=True)
    phone = db.Column(db.String(10),nullable=False,index=True)
    neighborhood = db.Column(db.String(64),nullable=False,index=True)
    website = db.Column(db.String(64),nullable=False,index=True)
    items = db.relationship('Item',backref='locations')

    def __repr__(self):
        return f"{self.name} -- {self.address} -- {self.phone} -- {self.website}"

