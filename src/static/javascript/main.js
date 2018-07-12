import Vue from 'vue';

let vm = new Vue({
    el: '#app',

    data: {

    },

    components: {

    },

    async beforeMount() {
        console.log('vue-start it up!')
    },

    methods: {

    }
});

// Make Vue instance accessible in console for debugging
window.vm = vm;
