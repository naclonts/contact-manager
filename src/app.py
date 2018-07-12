import os
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables file
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
load_dotenv(os.path.join(APP_ROOT, '.env'))

app = Flask(__name__)

@app.route('/')
def main_view():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
