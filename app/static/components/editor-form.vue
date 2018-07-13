/**
 * Modal form to add a new contact.
 */
<template>
<div class="new-contact">
    <div class="modal">
        <h2>Add/Edit Contact</h2>

        <input v-model="contact.first_name" placeholder="First name" />

        <input v-model="contact.last_name" placeholder="Last name" />

        <br />

        <label>Birthday</label>
        <input v-model="contact.date_of_birth" placeholder="Birthday"
            type="date"
        />

        <br />

        <label>Addresses</label>
        <input placeholder="Address 1" />
        <input placeholder="Address 2" />
        <input placeholder="Address 3" />


        <div class="button-wrapper">
            <button @click="save" class="save">Save</button>
            <button @click="cancel" class="cancel">Cancel</button>
        </div>
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
    display: flex;
    flex-direction: column;
    background-color: hsl(216, 66%, 12%);
    margin: 4em auto;
    max-width: 20em;
    padding: 1em;
    border-radius: 4px;
}
.modal > * {
    margin: 1em auto;
    width: 100%;
    line-height: 1.5em;
}
.modal h2 {
    margin: 0 auto 0.5em auto;
}
.modal label {
    font-size: 0.75em;
    margin: 0;
    color: #666;
}
.modal .button-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.modal .button-wrapper button {
    width: 45%;
}
</style>
