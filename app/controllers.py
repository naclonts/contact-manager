from flask import Blueprint, render_template, jsonify, request, make_response, \
                session
from app.models import User, Contact, model_to_dict
from app import db

router = Blueprint('routes', __name__)

@router.route('/')
def main_view():
    response = make_response(render_template('index.html'))
    user = None
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user: print('Found user! ID {0}'.format(user.id))
    if user is None:
        user = User()
        db.session.add(user)
        db.session.commit()
        session['user_id'] = str(user.id)
        session.modified = True
        session.permanent = True
        print('set session uid to {0}'.format(session['user_id']))
    return response

@router.route('/api/contacts', methods=['GET', 'POST'])
def get_contacts():
    user = User.query.filter_by(id=session['user_id']).first()
    # `Get` requests return list of contacts for user
    if request.method == 'GET':
        contacts = Contact.query.filter_by(user_id=user.id).all()
        return jsonify([model_to_dict(c) for c in contacts])
    # `Post` requests add a new contact
    elif request.method == 'POST':
        c = request.json['contact']
        contact = Contact(first_name=c['firstName'], last_name=c['lastName'])
        user.contacts.append(contact)
        db.session.commit()
        return jsonify({ 'message': 'POST successful!' })
