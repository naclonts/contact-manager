import os
from models import user
from flask import Flask, render_template, jsonify, request, make_response, \
                  session
from dotenv import load_dotenv

# Load environment variables file
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
load_dotenv(os.path.join(APP_ROOT, '.env'))

app = Flask(__name__)

@app.route('/')
def main_view():
    response = make_response(render_template('index.html'))
    print(session)
    if not 'user_id' in session:
        u = user.User()
        user_id = u.id
        session['user_id'] = str(user_id)
        session.modified = True
        session.permanent = True
        print('set session uid to {0}'.format(session['user_id']))
    return response

@app.route('/api/contacts', methods=['GET', 'POST'])
def get_contacts():
    if request.method == 'GET':
        print(session)
        if not 'user_id' in session:
            print('uid not found!')
            return jsonify([])
        user_id = session['user_id']
        print('Contacts request from {0}'.format(user_id))
        return jsonify([1, 2, 3, 42])
    elif request.method == 'POST':
        print(request.json)
        return jsonify({ 'message': 'POST successful!' })

if __name__ == '__main__':
    print(os.getenv('SECRET_KEY'))
    app.secret_key = os.getenv('SECRET_KEY')
    app.run()
