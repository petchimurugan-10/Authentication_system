from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config


app=Flask(__name__)
app.config.from_object(Config)

mongo=PyMongo(app)
bcrypt=Bcrypt(app)
jwt=JWTManager(app)
CORS(app)

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

app.register_blueprint(auth_bp,url_prefix='/auth')
app.register_blueprint(user_bp,url_prefix='/user')

if __name__=='__main__':
    with app.app_context():
        mongo.db.users.create_index("email", unique=True)

    app.run(debug=True)
# This will run the Flask application with debug mode enabled.
