from site import USER_BASE
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from bson.objectid import ObjectId
from utils.oauth_utils import GoogleOAuth

auth_bp=Blueprint('auth',__name__)
USER_BASE = Blueprint('user_base', __name__)

@USER_BASE.route('/register', methods=['POST'])
def register():
    mongo = current_app.extensions['pymongo']  # or current_app.mongo if assigned explicitly
    bcrypt = current_app.extensions['bcrypt']
    data = request.get_json()
    email = data.get('email')
    existing_user = mongo.db.users.find_one({'email': email})
    if existing_user:
        return jsonify({'error': 'Email already registered'})
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = {
        'username': data['username'],
        'email': email,
        'password': hashed_pw,
        'role': 'user'
    }
    mongo.db.users.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    mongo = current_app.extensions['pymongo']  # or current_app.mongo if assigned explicitly
    bcrypt = current_app.extensions['bcrypt']
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

@auth_bp.route('/oauth/google', methods=['POST'])
def google_oauth():
    data = request.get_json()
    token = data.get('token')
    mongo = current_app.extensions['pymongo']  # or current_app.mongo if assigned explicitly
    bcrypt = current_app.extensions['bcrypt']
    oauth = GoogleOAuth()
    user_info = oauth.verify_token(token)
    
    if user_info:
        # Check if user exists or create new user
        user = mongo.db.users.find_one({'email': user_info['email']})
        if not user:
            user = {
                'username': user_info['name'],
                'email': user_info['email'],
                'google_id': user_info['sub'],
                'role': 'user',
                'auth_provider': 'google'
            }
            mongo.db.users.insert_one(user)
        
        access_token = create_access_token(identity={
            'id': str(user['_id']),
            'email': user['email'],
            'role': user.get('role', 'user')
        })
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'error': 'Invalid Google token'}), 401

@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()
    mongo = current_app.extensions['pymongo']  # or current_app.mongo if assigned explicitly
    bcrypt = current_app.extensions['bcrypt']
    if current_user.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    users = list(mongo.db.users.find({}, {'password': 0}))
    for user in users:
        user['_id'] = str(user['_id'])
    
    return jsonify({'users': users}), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_token})