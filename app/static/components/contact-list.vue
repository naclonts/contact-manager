/**
 * Component that displays a list of contacts.
 */
<template>
<div class="contact-list">
    <button @click="openEditor(null)"
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
                    <td>
                        First Name
                    </td>
                    <td>
                        Last Name
                    </td>
                    <td>
                        Edit
                    </td>
                </tr>
            </thead>
        </table>

        <table class="body-table">
            <tbody>
                <tr v-for="contact in contacts">
                    <td>
                        {{ contact.first_name }}
                    </td>
                    <td>
                        {{ contact.last_name }}
                    </td>
                    <td>
                        <button
                            @click="openEditor(contact)"
                        >Edit</button>
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

export default {
    props: {
        contacts: Array
    },

    data() {
        return {
            showEditorForm: false,
            editingContact: {}
        }
    },

    methods: {
        openEditor: function(contact) {
            this.editingContact = contact;
            this.showEditorForm = true;
        },
        saveForm: async function(contact) {
            console.log(await api.updateContact(contact));
            this.showEditorForm = false;
        },
        cancelForm: function() {
            this.showEditorForm = false;
        }
    },

    components: {
        'editor-form': EditorForm
    }
}
</script>


<style scoped>
button {
    font-size: 1.5em;
    width: 1em;
    height: 1em;
}
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
.head-table {
    position: absolute;
    z-index: 1;
}
.body-table {
    margin-top: 1em;
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
