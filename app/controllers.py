"""
This module defines routes, including the main page view and API endpoints
for CRUD'ing contacts.
"""

from flask import Blueprint, render_template, jsonify, request, make_response, \
                session
from app.models import User, Contact, model_to_dict
from app import db

# Define as a Blueprint for Flask modularity
router = Blueprint('routes', __name__)

# Main page view
@router.route('/')
def main_view():
    response = make_response(render_template('index.html'))
    user = None
    # Get current user
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user: print('Found user! ID {0}'.format(user.id))
        else: print('User ID not found! ID {0}'.format(user.id))
    # Create user session if non-existent
    if user is None:
        user = User()
        db.session.add(user)
        db.session.commit()
        session['user_id'] = str(user.id)
        session.modified = True
        session.permanent = True
        print('set session uid to {0}'.format(session['user_id']))
    return response

# API routes for CRUD actions on contacts
@router.route('/api/contacts', methods=['GET', 'POST', 'PUT', 'DELETE'])
def contacts_api():
    user = User.query.filter_by(id=session['user_id']).first()
    # GET: return list of contacts
    if request.method == 'GET':
        return get_contacts(user)
    # POST: add a new contact
    elif request.method == 'POST':
        return add_contact(user, request.json['contact'])
    # PUT: replace an existing contact
    elif request.method == 'PUT':
        return update_contact(request.json['contact'])
    # DELETE: bye!
    elif request.method == 'DELETE':
        return delete_contact(request.json['contact'])


def get_contacts(user):
    contacts = Contact.query.filter_by(user_id=user.id).all()
    return jsonify([model_to_dict(c) for c in contacts])

def add_contact(user, c):
    contact = Contact(**c) # unpack dict `c` to model class parameters
    user.contacts.append(contact)
    db.session.commit()
    return jsonify({ 'id': contact.id, 'message': 'POST successful!' })

def delete_contact(c):
    Contact.query.filter_by(id = c['id']).delete()
    db.session.commit()
    return jsonify({ 'message': 'Contact deleted.' })

def update_contact(contact_dict):
    contact = Contact.query.get(contact_dict['id'])

    # Assign JSON fields to model
    for key, val in contact_dict.items():
        setattr(contact, key, val)

    # Save the changes
    db.session.commit()

    return jsonify({ 'message': 'Contact updated!' })
