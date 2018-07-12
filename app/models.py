"""This module manages contact information, including saving and retrieving data."""

import uuid
import sys
from sqlalchemy.dialects.postgresql import ARRAY
from app import db


class User(db.Model):
    """A user."""
    id = db.Column(db.Integer, primary_key=True)
    contacts = db.relationship('Contact', backref='user', lazy=True)

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def add_contact(self, contact):
        self.contacts.push(contact)

    def get_contacts(self):
        return self.contacts

    def remove_contact(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return self.contacts.remove(contact)
        print('No contact found with ID {0}'.format(contact_id))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    addresses = db.Column(ARRAY(db.String(200)), nullable=True)
    # phone_numbers = db.Column(db.Array(db.String(30)), nullable=True)
    # emails = db.Column(db.Array(db.String(120)), nullable=True)

    # Parent User who created this contact
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Contact {0} {1}>'.format(self.first_name, self.last_name)


def model_to_dict(model):
    """Returns a simple (serializable) dictionary from a SQLAlchemy object."""
    d = {}
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        d[col.name] = getattr(model, col.name)
    return d
