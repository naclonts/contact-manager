/**
 * Display an editable list of contacts, with a search box and export feature.
 */
<template>
<div class="contact-list">
    <!-- Add Contact and Search input -->
    <button class="add-contact green"
        @click="edit(newContact)"
        title="Add contact"
    >+</button>
    <div class="search">
        <i class="fas fa-search"></i>
        <input class="search-input" v-model="searchText"
            placeholder="Search"
        />
    </div>

    <!-- Editor modal when contacts are viewed or modified -->
    <editor-form v-if="showEditorForm"
        :contact="editingContact"
        :startInEditMode="openContactInEditMode"
        @save="saveForm"
        @cancel="cancelForm"
    ></editor-form>

    <!-- The list itself -->
    <div class="table-wrapper">
        <table>
            <thead>
                All Contacts
            </thead>
            <tbody>
                <tr v-for="contact in contacts"
                    v-show="visible(contact)"
                    @mouseover="hoveringContactId=contact.id"
                    @mouseleave="hoveringContactId=null"
                >
                    <td @click="view(contact)">
                        {{ contact.first_name }} {{ contact.last_name }}
                    </td>
                    <td v-if="bigScreen" @click="view(contact)">
                        {{ contact.phone_numbers ? contact.phone_numbers[0] : '' }}
                    </td>
                    <td>
                        <div class="button-wrapper">
                            <button @click="edit(contact)"
                                v-show="hoveringOver(contact) || !bigScreen">
                                <i class="fas fa-pen" title="Edit contact"></i>
                            </button>
                            <button @click="deleteContact(contact)"
                                v-show="hoveringOver(contact) || !bigScreen">
                                <i class="fas fa-trash" title="Remove contact"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Show Undo option when contacts are deleted -->
    <div v-if="showUndo" class="undo-box">
        <p>Contact Deleted.</p>
        <button @click="cancelDelete()">Undo</button>
    </div>

</div>
</template>

<script>
'use strict';

import * as api from '../javascript/api';
import EditorForm from './editor-form.vue';
const clone = require('ramda/src/clone');


export default {
    data() {
        return {
            contacts: [],
            showEditorForm: false,
            openContactInEditMode: true,
            editingContact: {},
            searchText: '',
            hoveringContactId: null,
            windowWidth: 0,
            showUndo: false,
            deletedContacts: [],
            deletedTimeouts: []
        }
    },

    components: {
        'editor-form': EditorForm
    },

    // Load contacts when mounted
    async mounted() {
        // Get user's contacts and sort by name
        let contactList = await api.getContacts();
        contactList.sort((a, b) => {
            return a.first_name.toLowerCase() < b.first_name.toLowerCase()
                ? -1 : +1;
        });
        this.contacts = contactList;
        if (this.contacts.length == 0) this.$emit('no-contacts-loaded');

        // Listen for window resizes to adjust displayed columns
        window.addEventListener('resize', this.resize);
        this.resize();
    },

    beforeDestroy() {
        window.removeEventListener('resize', this.resize);
    },

    computed: {
        newContact: function() {
            return {};
        },
        // Check for displaying phone number field in list
        bigScreen: function() {
            return this.windowWidth > 700;
        }
    },

    methods: {
        // Methods to view and edit contact
        view: function(contact) {
            this.openEditor(contact, false);
        },
        edit: function(contact) {
            this.openEditor(contact, true);
        },
        openEditor: function(contact, openInEditMode=true) {
            this.openContactInEditMode = openInEditMode;
            this.editingContact = clone(contact);
            this.showEditorForm = true;
        },

        // Save an updated contact to the server
        saveForm: async function(contact) {
            let i = this.index(contact);
            // If this contact already exists, update it
            if (i > -1) {
                // Update on server
                console.log(await api.updateContact(contact));
                // Update in this component
                this.contacts[i] = contact;
            // If this contact doesn't exist, add it
            } else {
                contact.color = randomColor();
                let res = await api.addContact(contact);
                console.log(res.message);
                contact.id = res.id;
                this.contacts.push(contact);
            }
            // Exit modal
            this.showEditorForm = false;
        },

        // Close modal without saving
        cancelForm: function() {
            this.showEditorForm = false;
        },

        // Delete contact. Gives 3 seconds before actually deleting from server,
        // giving user chance to undo.
        deleteContact: function(contact) {
            this.contacts.splice(this.index(contact), 1);
            this.showUndo = true;
            this.deletedContacts.push(contact);
            this.deletedTimeouts.push(
                setTimeout(this.deleteFromServer.bind(this), 5000)
            );
        },
        // Actually delete from server if user hasn't undone action
        deleteFromServer: async function(contact) {
            this.showUndo = false;
            clearTimeout(this.deletedTimeouts.shift());
            await api.deleteContact(this.deletedContacts.shift());
        },
        // Undo delete action
        cancelDelete: function() {
            clearTimeout(this.deletedTimeouts.shift());
            this.contacts.push(this.deletedContacts.shift());
            if (this.deletedContacts.length == 0) this.showUndo = false;
        },

        index: function(contact) {
            return this.contacts.findIndex((c) => c.id == contact.id);
        },

        /**
         * Check if contact should be displayed, based on current search text.
         * @param  {Contact} contact
         * @return {Boolean} true if contact should be displayed
         */
        visible: function(contact) {
            let text = this.searchText.toLowerCase();
            // Show everything when there hasn't been a search
            if (text == '') return true;
            // Functions to check if field is a match
            function match(str) {
                if (!str) return false;
                return str.toLowerCase().includes(text);
            }
            function matchArray(arr) {
                if (!arr) return false;
                return arr.filter(match).length > 0;
            }
            // Check if search text matches any field
            return match(contact.first_name) || match(contact.last_name)
                || match(contact.date_of_birth)
                || matchArray(contact.addresses)
                || matchArray(contact.phone_numbers)
                || matchArray(contact.emails);
        },

        hoveringOver: function(contact) {
            return this.hoveringContactId == contact.id;
        },

        resize: function() {
            this.windowWidth = window.innerWidth;
        }
    }
}


function randomColor() {
    let colors = [
        'cadetblue', 'chocolate', 'darkblue', 'darkgreen', 'darkorchid',
        'darksalmon', 'darkviolet', 'gray', 'orangered', 'seagreen', 'tomato'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}
</script>


<style scoped>
/****************************************************************************/
/* Input Styles */
.contact-list {
    margin: 1em;
}
.search {
    display: inline-block;
    height: 1.6em;
    font-size: 1.25em;
    border-bottom: 1px solid hsl(89, 100%, 50%);
    margin: 0.5em;
    margin-bottom: 0;
}
.search input {
    width: calc(100% - 3em);
    border: none;
    margin: 0.25em;
    margin-bottom: 0;
}
.search:focus-within {
    background-color: #555;
}
button.add-contact {
    font-size: 1.5em;
    position: fixed;
    bottom: 1em;
    right: 1em;
    z-index: 1;
}

/* Wrapper for contact-editing buttons that show up on hover */
.button-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    width: 100%;
    height: 100%;
}
.button-wrapper button {
    background-color: transparent;
    line-height: 1em;
    height: 1em;
    font-size: 1em;
    color: white;
}
.button-wrapper button:hover {
    color: hsl(89, 100%, 55%);
}

/****************************************************************************/
/* Table Styles */
.table-wrapper {
    position: relative;
}
table {
    table-layout: fixed;
    border-collapse: collapse;
    position: relative;
    margin-top: 2em;
    font-size: 1.1em;
}
.table-wrapper, table {
    width: 100%;
}
table tr {
    width: 100%;
    text-transform: capitalize;
    height: 2.5em;
}
table tbody tr {
    cursor: pointer;
    padding-top: 1em;
}
/* Light up row when user hovers */
table tbody tr:hover {
    background-color: #444;
}
table tr td {
    padding-top: 0.5em;
    padding-bottom: 0.5em;
}
/* Header style */
thead {
    font-size: 1.2em;
    color: hsl(89, 100%, 72%);
    border-bottom: 1px solid hsl(89, 35%, 28%);
    border-spacing: 0;
    padding-bottom: 0;
}
/* Icons */
table i {
    font-size: 0.9em;
}

/* Box to undo delete */
.undo-box {
    position: fixed;
    right: 1em;
    top: 1em;
    border-radius: 2px;
    padding: 1em;
    z-index: 10;
    background-color: white;
    color: #333;
}
.undo-box button {
    border-radius: 2px;
    padding: 4px;
}
</style>
