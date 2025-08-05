from flask import Blueprint, request, jsonify
from app import mongo, bcrypt
from flask_jwt_extended import create_access_token
from bson.objectid import ObjectId

auth_bp=Blueprint('auth',__name__)
def register():
    data=request.get_json()
    email=data.get('email')
    existing_user=mongo.db.users.find_one({'email':email})
    if existing_user:
        return jsonify({'error':'Email already registered'})
    hashed_pw=bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user={
        'username':data['username'],
        'email':email,
        'password':hashed_pw,
        'role':'user'
    }
    mongo.db.users.insert_one(user)
    return jsonify({'message':'User registered successfully'}),201

@auth_bp.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')

    user = mongo.db.users.find_one({'email': email})
    if user and bcrypt.check_password_hash(user['password'],password):
        access_token=create_access_token(identity={
            'id':str(user['_id']),
            'email':user['email'],
            'role':user.get('role','user')
        })
        return jsonify({'access_token':access_token}),200
    return jsonify({'error':'Invalid email or password'}),401
