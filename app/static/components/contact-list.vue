/**
 * Component that displays a list of contacts.
 */
<template>
<div class="contact-list">
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

    <editor-form v-if="showEditorForm"
        :contact="editingContact"
        :startInEditMode="openContactInEditMode"
        @save="saveForm"
        @cancel="cancelForm"
    ></editor-form>

    <div class="table-wrapper">
        <table>
            <thead>
                All Contacts
            </thead>
            <tbody>
                <tr v-for="contact in contacts"
                    v-if="visible(contact)"
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
                                v-show="hoveringOver(contact)">
                                <i class="fas fa-pen" title="Edit contact"></i>
                            </button>
                            <button @click="deleteContact(contact)"
                                v-show="hoveringOver(contact)">
                                <i class="fas fa-trash" title="Remove contact"></i>
                            </button>
                        </div>
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
const clone = require('ramda/src/clone');

export default {
    data() {
        return {
            contacts: [],
            showEditorForm: false,
            openContactInEditMode: true,
            editingContact: {},
            timeoutId: null,
            searchText: '',
            hoveringContactId: null,
            windowWidth: 0
        }
    },

    components: {
        'editor-form': EditorForm
    },

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
        bigScreen: function() {
            return this.windowWidth > 700;
        }
    },

    methods: {
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
    border: none;
    margin: 0.25em;
    margin-bottom: 0;
}
.search:focus-within {
    background-color: #555;
}
button.add-contact {
    font-size: 1.5em;
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
    color: hsl(89, 43%, 84%);
    border-bottom: 1px solid hsl(89, 35%, 28%);
    border-spacing: 0;
    padding-bottom: 0;
}
/* Icons */
table i {
    font-size: 0.9em;
}
/* Initial of first name */
.initial-cell {
    width: 1em;
}
.initial-cell div {
    width: 2em;
    background-color: blue;
    color: inherit;
    border-radius: 50%;
}
.initial-cell h1 {
    width: 1em;
    height: 1em;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 6px 0 0 1px;
}
</style>
