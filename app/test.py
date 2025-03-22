from app import app, mongo
from flask import Blueprint

tm_bp = Blueprint('tm', __name__)

@app.route('/test-mongo')
def test_mongo():
    try:
        mongo.db.command('ping')
        return "MongoDB connection successful!"
    except Exception as e:
        return str(e)