/**
 * Component that displays a list of contacts.
 */
<template>
<div class="contact-list">
    <table class="head-table">
        <thead>
            <tr>
                <td>
                    First Name
                </td>
                <td>
                    Last Name
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
.contact-list {
    margin: 1em;
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
