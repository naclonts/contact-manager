'use strict';

import Vue from 'vue';
import * as api from './api';
import ContactList from '../components/contact-list.vue';
import Welcome from '../components/welcome.vue';

let vm = new Vue({
    el: '#app',

    data: {
        showWelcomeScreen: false
    },

    components: {
        'contact-list': ContactList,
        'welcome': Welcome
    }
});
