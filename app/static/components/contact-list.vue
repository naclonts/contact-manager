/**
 * Component that displays a list of contacts.
 */
<template>
<div class="contact-list">
    <button @click="showNewContactForm=true"
    >+</button>

    <new-contact-form v-if="showNewContactForm"
        @cancel="cancelForm"
    ></new-contact-form>

    <div class="table-wrapper">
        <table class="head-table">
            <thead>
                <tr>
                    <td>
                        First Name
                    </td>
                    <td>
                        Last Named
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
                </tr>
            </tbody>
        </table>
    </div>




</div>
</template>

<script>
'use strict';
import NewContactForm from './new-contact-form.vue';

export default {
    props: {
        contacts: Array
    },

    data() {
        return {
            showNewContactForm: false
        }
    },

    methods: {
        cancelForm: function() {
            this.showNewContactForm = false;
        }
    },

    components: {
        'new-contact-form': NewContactForm
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
