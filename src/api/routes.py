"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Photo, Order, OrderItems
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)
 
@api.route('/users', methods = ['GET'])
def get_users(): 
    users = User.query.all()
    users_serialized = list(map(lambda item:item.serialize(), users))
    response_body = {
        "message" : "Nice!",
        "data": users_serialized
    }
    if (users == []):
        return jsonify({"msg": "Not users yet"}), 404
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>', methods = ['GET'])
def get_user(user_id): 
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
        
    user_info = User.query.filter_by(id=user_id).first().serialize()    
    response_body = {
        "message" : "Nice!",
        "data": user_info
    }

    return jsonify(response_body), 200

@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    users_query = User.query.filter_by(email=email).first()
    if not users_query:
        return jsonify({"msg": "Doesn't exist"}), 402
    if password != users_query.password:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@api.route('/register', methods=['POST'])
def register():
    request_body = request.get_json()

    if User.query.filter_by(email=request_body["email"]).first():
        return jsonify({"msg": "Email already exists"}), 409
   
    user = User()
    user.new_user(
        email=request_body["email"],    
        password=request_body["password"],
        username=request_body["username"],
        name = request_body["name"],
        firstname = request_body["firstname"],
        role = request_body["role"]
    )

    access_token = create_access_token(identity=request_body["email"])
    return jsonify(access_token=access_token), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        User.query.filter_by(id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted"}), 200
    else:
        return jsonify({"msg": "User doesn't exist"}), 401
    
@api.route('/photos', methods=['POST'])
def new_photo():
    request_body = request.get_json()

    if Photo.query.filter_by(id=request_body["id"]).first():
        return jsonify({"msg": "Duplicated image"}), 409

    photo = Photo()
    photo.new_photo(
        id=request_body["id"],    
        url=request_body["url"],
        bicycle=request_body["bicycle"],
        helmet = request_body["helmet"],
        price = request_body["price"],
        #user_id = request_body["user_id"] PREGUNTAR
    )

    db.session.add(new_photo)
    db.session.commit()

    return jsonify({"msg": "Photo created", "photo": new_photo.serialize()}),201

@api.route('/photos', methods = ['GET'])
def get_photos(): 
    photos = Photo.query.all()
    photos_serialized = list(map(lambda item:item.serialize(), photos))
    response_body = {
        "message" : "Nice photos!",
        "data": photos_serialized
    }
    if (photos == []):
        return jsonify({"msg": "Not photos yet"}), 404
    return jsonify(response_body), 200

@api.route('/photos/<int:photo_id>', methods = ['GET'])
def get_photo(photo_id): 
    photo = Photo.query.get(photo_id)
    if photo is None:
        return jsonify({"msg": "Photo not found"}), 404
        
    photo_info = Photo.query.filter_by(id=photo_id).first().serialize()
    response_body = {
        "message" : "Nice photo!",
        "data": photo_info
    }

    return jsonify(response_body), 200

@api.route('/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    photo = Photo.query.get(photo_id)
    if photo:
        Photo.query.filter_by(id=photo_id).delete()
        db.session.delete(photo)
        db.session.commit()
        return jsonify({"msg": "Photo deleted"}), 200
    else:
        return jsonify({"msg": "Photo doesn't exist"}),401
        user_id = request_body["user_id"]

@api.route('/orders', methods=['POST'])
def new_order():
    request_body = request.get_json()
    if Order.query.filter_by(id=request_body["id"]).first():
        return jsonify({"msg": "Duplicated order"}), 409
    order = Order(
        id=request_body["id"],
        status=request_body["status"],
        payment_method=request_body["payment_method"],
        user_id=request_body["user_id"]
    )
    db.session.add(order)
    db.session.commit()

    return jsonify({"msg": "Order created", "order": order.serialize()}), 201


@api.route('/orders', methods = ['GET'])
def get_orders(): 
    orders = Order.query.all()
    orders_serialized = list(map(lambda item:item.serialize(), orders))
    response_body = {
        "message" : "ok!",
        "data": orders_serialized
    }
    if (get_orders == []):
        return jsonify({"msg": "Not orders yet"}), 404
    return jsonify(response_body), 200



@api.route('/orders/<int:order_id>', methods = ['GET'])
def get_order(order_id): 
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"msg": "Order not found"}), 404
        
    order_info = Order.query.filter_by(id=order_id).first().serialize()    
    response_body = {
        "message" : "ok!",
        "data": order_info
    }

    return jsonify(response_body), 200


@api.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        Order.query.filter_by(id=order_id).delete()
        db.session.delete(order)
        db.session.commit()
        return jsonify({"msg": "Order deleted"}), 200
    else:
        return jsonify({"msg": "Order doesn't exist"}), 401
    





