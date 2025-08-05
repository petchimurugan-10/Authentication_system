from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp=Blueprint('user',__name__)
@user_bp.route('/profile',methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    return jsonify({
        'message':'User profile retrieved successfully',
        'user':current_user
    })
