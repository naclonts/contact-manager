from flask import Blueprint, render_template, jsonify, request, make_response, \
                session

from app.models import User
from app import db

router = Blueprint('routes', __name__)

@router.route('/')
def main_view():
    response = make_response(render_template('index.html'))
    user = None
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        print('Found user! ID {0}'.format(user.id))
    if user is None:
        user = User(username='test username')
        db.session.add(user)
        db.session.commit()
        session['user_id'] = str(user.id)
        session.modified = True
        session.permanent = True
        print('set session uid to {0}'.format(session['user_id']))
    return response

@router.route('/api/contacts', methods=['GET', 'POST'])
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
