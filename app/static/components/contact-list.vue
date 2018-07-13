/**
 * Component that displays a list of contacts.
 */
<template>
<div class="contact-list">
    <button @click="openEditor(newContact)"
    >+</button>

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
                <tr v-for="contact in contacts">
                    <td>{{ contact.first_name }}</td>
                    <td>{{ contact.last_name }}</td>
                    <td>{{ formatDate(contact.date_of_birth) }}</td>
                    <td><button
                            @click="openEditor(contact)"
                        >Edit</button>
                    </td>
                    <td><button
                            @click="deleteContact(contact)"
                        >X</button>
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
import { clone } from 'ramda';
import * as moment from 'moment';

export default {
    data() {
        return {
            contacts: [],
            showEditorForm: false,
            editingContact: {},
            timeoutId: null
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
            return ['First Name', 'Last Name', 'Birthday', 'Edit', 'Delete'];
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
        }
    }
}
</script>


<style scoped>
.contact-list {
    margin: 1em;
}
.table-wrapper {
    background-color: #333;
    border-radius: 8px;
    max-height: 80vh;
    overflow-y: scroll;
}
table {
    border-collapse: collapse;
    position: relative;
}
table tr td {
    padding-top: 0.5em;
    padding-bottom: 0.5em;
}
.head-table {
    position: absolute;
    z-index: 1;
    height: 2em;
}
.body-table {
    margin-top: 2em;
    position: relative;
}
thead {
    display: table-header-group;
    background-color: #555;
}
td {
    width: 8em;
}

</style>
