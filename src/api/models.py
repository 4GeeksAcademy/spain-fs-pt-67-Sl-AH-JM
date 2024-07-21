from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled'), nullable=False)
    payment_method = db.Column(db.Enum('credit_card', 'paypal', 'cash'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    bicycle = db.Column(db.Enum('mountain', 'road', 'hybrid'), nullable=False)
    helmet = db.Column(db.Enum('full_face', 'open_face', 'modular'), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('photos', lazy=True))

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    photo = db.relationship('Photo', backref=db.backref('order_items', lazy=True))
