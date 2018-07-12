"""This module manages contact information, including saving and retrieving data."""

import uuid

class User:
    """A user."""
    def __init__(self):
        self.contacts = []
        self.id = uuid.uuid4()

    def add_contact(self, contact):
        self.contacts.push(contact)

    def get_contacts(self):
        return self.contacts

    def remove_contact(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return self.contacts.remove(contact)
        print('No contact found with ID {0}'.format(contact_id))

def get_user(id_str):
    pass
