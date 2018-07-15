import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.json import JSONEncoder
from datetime import date
from dotenv import load_dotenv

# Load environment variables file
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
load_dotenv(os.path.join(APP_ROOT, '.env'))

app = Flask('app')
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define JSON encoding class to encode dates in ISO format
class JSONEncoderISODate(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
app.json_encoder = JSONEncoderISODate

# Not found page
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.controllers import router
app.register_blueprint(router)

db.create_all()
