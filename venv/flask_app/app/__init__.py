from flask import Flask
from app.config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, MONGO_CONN_URL
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['MONGO_URI'] = MONGO_CONN_URL
app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')

mongo = PyMongo(app)

csrf = CSRFProtect(app)

db = SQLAlchemy(app)

ALLOWED_IMAGE_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

from app.routes.auth_routes import auth_bp
from app.routes.home_route import home_bp
from app.routes.password_routes import pw_bp
from app.routes.articles_routes import art_bp
from app.routes.admin import admin_bp
from app.test import tm_bp


app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(pw_bp)
app.register_blueprint(art_bp)
app.register_blueprint(tm_bp)
app.register_blueprint(admin_bp)

from app.models import User
