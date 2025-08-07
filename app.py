from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth_routes import USER_BASE


# app.py or __init__.py in a package

mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # or from_envvar, from_pyfile, etc

    # Initialize extensions with app instance
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints here, after app creation
    from routes.auth_routes import auth_bp, USER_BASE
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(USER_BASE, url_prefix='/user')

    return app

