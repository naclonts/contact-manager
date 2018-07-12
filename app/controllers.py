from flask import Blueprint, render_template, jsonify, request, make_response, \
                session
from json import dumps
from app.models import User, Contact
from app import db

router = Blueprint('routes', __name__)

def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object.
    """
    json = {}

    for col in model._sa_class_manager.mapper.mapped_table.columns:
        json[col.name] = getattr(model, col.name)

    return dumps(json)

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
    if request.method == 'GET':
        print('Contacts request from {0}'.format(session['user_id']))
        contacts = Contact.query.filter_by(user_id=user.id).all()
        return dumps([to_json(c) for c in contacts])
    elif request.method == 'POST':
        c = request.json['contact']
        contact = Contact(first_name=c['firstName'], last_name=c['lastName'])
        user.contacts.append(contact)
        db.session.commit()
        return jsonify({ 'message': 'POST successful!' })
