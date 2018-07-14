/**
 * Component that displays a list of contacts.
 */
<template>
<div class="contact-list">
    <button class="add-contact"
        @click="openEditor(newContact)"
        title="Add contact"
    >+</button>
    <input class="search" v-model="searchText" />

    <editor-form v-if="showEditorForm"
        :contact="editingContact"
        @save="saveForm"
        @cancel="cancelForm"
    ></editor-form>

    <div class="table-wrapper">
        <table class="head-table">
            <thead>
                <tr>
                    <td v-for="header in headers"
                        @click="sortByHeader(header)">
                        {{ header }}
                    </td>
                </tr>
                <tr>

                </tr>
            </thead>
        </table>

        <table class="body-table">
            <tbody>
                <tr v-for="contact in contacts"
                    v-if="visible(contact)"
                    @click="viewDetail(contact)"
                    @mouseover="hoveringContactId=contact.id"
                    @mouseleave="hoveringContactId=null"
                >
                    <td>{{ contact.first_name }}</td>
                    <td>{{ contact.last_name }}</td>
                    <td>{{ formatDate(contact.date_of_birth) }}</td>
                    <td class="button-wrapper" v-if="hoveringOver(contact)">
                        <button @click="openEditor(contact)">
                            <i class="fas fa-pen" title="Edit contact"></i>
                        </button>
                        <button @click="deleteContact(contact)">
                            <i class="fas fa-trash" title="Remove contact"></i>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

</div>
</template>

<script>
'use strict';
import * as api from '../javascript/api';
import EditorForm from './editor-form.vue';
import * as moment from 'moment';
const clone = require('ramda/src/clone');

export default {
    data() {
        return {
            contacts: [],
            showEditorForm: false,
            editingContact: {},
            timeoutId: null,
            searchText: '',
            hoveringContactId: null
        }
    },

    components: {
        'editor-form': EditorForm
    },

    async mounted() {
        console.log('Mounted contact list')
        this.contacts = await api.getContacts();
    },

    computed: {
        newContact: function() {
            return {};
        },
        headers: function() {
            return ['First Name', 'Last Name', 'Birthday', 'Edit'];
        }
    },

    methods: {
        openEditor: function(contact) {
            this.editingContact = clone(contact);
            this.showEditorForm = true;
        },

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
                let res = await api.addContact(contact);
                console.log(res.message);
                contact.id = res.id;
                this.contacts.push(contact);
            }
            // Exit modal
            this.showEditorForm = false;
        },

        cancelForm: function() {
            this.showEditorForm = false;
        },

        deleteContact: function(contact) {
            // Delete from server after 3 seconds, to give user a chance to Undo
            async function trulyDelete() {
                console.log(await api.deleteContact(contact));
                this.timeoutId = null;
            }
            this.contacts.splice(this.index(contact), 1);
            this.timeoutId = setTimeout(trulyDelete, 3000);
        },

        index: function(contact) {
            return this.contacts.findIndex((c) => c.id == contact.id);
        },

        formatDate: function(date) {
            return moment(date).format('M/D/YYYY');
        },

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

        viewDetail: function(contact) {
            console.log(`View ${contact.first_name}`);
        },

        hoveringOver: function(contact) {
            return this.hoveringContactId == contact.id;
        }
    }
}
</script>


<style scoped>
.contact-list {
    margin: 1em;
}
.table-wrapper {
    position: relative;
    width: 100%;
}
table {
    border-collapse: collapse;
    position: relative;
}
input.search {
    font-size: 1.5em;
}
button.add-contact {
    font-size: 1.5em;
    background-color: hsl(89, 100%, 55%);
    box-shadow: 0 6px 10px 0 rgba(0,0,0,0.28),
                0 1px 18px 0 rgba(0,0,0,0.12),
                0 3px 5px -1px rgba(0,0,0,0.4);
}
button.add-contact:hover {
    background-color: hsl(89, 100%, 75%);
    box-shadow: 0 6px 10px 0 rgba(0,0,0,0.25),
                0 1px 18px 0 rgba(0,0,0,0.24),
                0 3px 5px -1px rgba(0,0,0,0.4);
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
/* Light up row when user hovers */
.body-table tr:hover {
    background-color: #444;
}
.body-table tr {
    cursor: pointer;
    text-transform: capitalize;
}
table tr td {
    padding-top: 0.5em;
    padding-bottom: 0.5em;
}
.head-table {
    position: absolute;
    z-index: 1;
    height: 2em;
    color: #ccc;
}
.body-table {
    position: absolute;
    top: 2em;
}
thead {
    display: table-header-group;
}
td {
    width: 8em;
}

</style>
