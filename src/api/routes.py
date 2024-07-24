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
    print ("AAAAAAAAAAAAAA", user)
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
