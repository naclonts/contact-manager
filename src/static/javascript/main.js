import Vue from 'vue';
import * as api from './api';

let vm = new Vue({
    el: '#app',

    data: {

    },

    components: {

    },

    async beforeMount() {
        console.log('vue-start it up!')
        let response = await api.addContact({
            firstName: 'dude', lastName: 'come on'
        });
        console.log(`Add contact response: ${response.message}`);

        let data = await api.getContacts();
        console.log(data);
    },

    methods: {

    }
});

// Make Vue instance accessible in console for debugging
window.vm = vm;
