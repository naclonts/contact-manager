<template>
<div class="welcome-screen">
    <h1>Contact Manager <em>Retro</em></h1>

    <div class="text-content">
        <p>
            This is an app to track your contacts, with a touch of old-school computing nostalgia.
        </p>
        <p>
            No login is required to use this site. Because of this, contacts entered will only show up on the device you enter them on.
        </p>
        <p>
            Enjoy!
        </p>
    </div>

    <button @click="$emit('exit-welcome')" class="green">Let's Go</button>
</div>
</template>

<script>
'use strict';

export default {
    mounted() {
        console.log('Welcome')
    }
}
</script>

<style scoped>
.welcome-screen {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    min-height: 100vh;
    background-color: hsl(240, 94%, 13%);
    z-index: 100;
    padding: 2em;
}
.welcome-screen * {
    margin: 1em 0;
}

.text-content {
    max-width: 750px;
}

em {
    color: hsl(89, 100%, 50%);
    font-style: normal;
}
button {
    padding: 0.5em;
    height: 2em;
}
</style>
