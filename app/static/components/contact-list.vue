/**
 * Component that displays a list of contacts.
 */
<template>
<div class="contact-list">
    <div v-for="contact in contacts">
        {{ contact.first_name }} {{ contact.last_name }}
    </div>
</div>
</template>

<script>
'use strict';

export default {
    props: {
        contacts: Array
    },

}
</script>


<style>
</style>
