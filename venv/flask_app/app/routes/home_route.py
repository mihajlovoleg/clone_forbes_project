from flask import render_template, Blueprint, session
from app import mongo

home_bp = Blueprint('home', __name__)

@home_bp.before_request
def check_role():
    if session.get('email') is None:
        session['role'] = 'guest'

@home_bp.route('/')
def home_page():
    
    print(session.get('role'))
    print(session.get('email'))
    articles = mongo.db.articles.find().sort('created_at', -1)
    return render_template('home.html', articles=articles, is_loginned=session.get('email'), name=session.get('name'), surname=session.get('surname'), user=session.get('role'))