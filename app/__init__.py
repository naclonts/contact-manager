import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables file
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
load_dotenv(os.path.join(APP_ROOT, '.env'))

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts-manager.db'
db = SQLAlchemy(app)

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

from app.controllers import router
app.register_blueprint(router)

db.create_all()
