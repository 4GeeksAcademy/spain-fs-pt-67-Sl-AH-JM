from flask_sqlalchemy import SQLAlchemy
import enum

class MyRoles(enum.Enum):
    photographer = "Photographer"
    rider = "Rider"
    admin = "Admin"

class StatusOrders(enum.Enum):
    pending = "Pending"
    completed = "Completed"
    cancelled = "Cancelled"

class PaymentMethods(enum.Enum):
    credit_card = "Credit_card"
    paypal = "Paypal"
    cash = "Cash"

class Bikes(enum.Enum):
    santa_Cruz = "Santa Cruz"
    orbea = "Orbea"
    canyon = "Canyon"
    custom = "Custom"

class Helmets(enum.Enum):
    scott = "Scott"
    troyLee = "TroyLee"
    bluegrass = "Bluegrass"
    custom = "Custom"


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum(MyRoles), nullable=False, default = MyRoles.rider)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(StatusOrders), nullable=False, default = StatusOrders.pending)
    payment_method = db.Column(db.Enum(PaymentMethods), nullable=False, default = PaymentMethods.credit_card)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    bicycle = db.Column(db.Enum(Bikes), nullable=False, default = Bikes.custom)
    helmet = db.Column(db.Enum(Helmets), nullable=False, default = Helmets.custom)
    price = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class OrderItems(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False) 
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'), nullable=False) 