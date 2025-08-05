from flask_jwt_extended import create_access_token

def generate_token(user):
    payload={
        "id":str(user['_id']),
        "email":user['email'],
        "role":user.get('role','user')
    }
    return create_access_token(identity=payload)
