/**
 * Modal form to add a new contact.
 */
<template>
<div class="new-contact">
    <div class="modal">
        <h2>Add/Edit Contact</h2>

        <input v-model="contact.first_name" placeholder="First name" />
        <input v-model="contact.last_name" placeholder="Last name" />
        <input v-model="contact.date_of_birth" placeholder="Birthday" />

        <button @click="save" class="save">Save</button>
        <button @click="cancel" class="cancel">Cancel</button>
    </div>
</div>
</template>


<script>
'use strict';

import { clone } from 'ramda';

export default {
    props: {
        contact: {
            type: Object,
            default: () => { return {} }
        }
    },

    methods: {
        save: function() {
            this.$emit('save', clone(this.contact));
        },
        cancel: function() {
            this.$emit('cancel');
        }
    }
}
</script>


<style scoped>
.new-contact {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 10;
    background-color: hsla(0, 0%, 70%, 0.5);
}
.modal {
    background-color: #333;
    margin: 4em;
    height: 8em;
}
.modal h2 {
    margin: auto;
}
</style>
