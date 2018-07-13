import Vue from 'vue';
import * as api from './api';
import ContactList from '../components/contact-list.vue';

let vm = new Vue({
    el: '#app',

    data: {
    },

    components: {
        'contact-list': ContactList
    },

    async beforeMount() {
        console.log('vue-start it up!')
        // let response = await api.addContact({
        //     firstName: 'dude', lastName: 'come on'
        // });

    }
});

// Make Vue instance accessible in console for debugging
window.vm = vm;
