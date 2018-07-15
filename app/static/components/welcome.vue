/**
 * Welcome screen for users who don't have any contacts, including any first-
 * time visitors.
 *
 */
<template>
<div class="welcome-screen">
    <div class="content-wrapper">
        <h1>Contact Manager <em>Retro</em></h1>

        <p>
            This is an app to track your contacts, with a touch of old-school computing nostalgia.
        </p>
        <p>
            No login is required to use this site. Because of this, contacts will only be seen on the device used to create them.
        </p>
        <p>
            Enjoy!
        </p>

        <div class="bottom-row">
            <button @click="$emit('exit-welcome')" class="green">Let's Go</button>

            <!-- Cat face! Skip on mobile. -->
            <svg v-if="prettyBigScreen" id="root-svg" ref="catFace"
                width="200" height="200" xmlns="http://www.w3.org/2000/svg">
                 <defs>
                     <linearGradient id="whisker-gradient"
                         x1="0%" y1="0%" x2="100%" y2="0%">
                         <stop offset="45%" stop-color="hsla(0, 0%, 83%, 0.6)" />
                         <stop offset="100%" stop-color="hsla(0, 2%, 18%, 0.6)" />
                     </linearGradient>
                     <linearGradient id="whisker-gradient-reverse"
                         x1="100%" y1="0%" x2="0%" y2="0%">
                         <stop offset="45%" stop-color="hsla(0, 0%, 83%, 0.6)" />
                         <stop offset="100%" stop-color="hsla(0, 2%, 18%, 0.6)" />
                     </linearGradient>
                 </defs>
             </svg>
        </div>

        <div class="footer">
            <p>
                More Perfect DOS VGA font by <a href="http://laemeur.sdf.org/" _target="blank">Adam Moore</a>.
            </p>
        </div>
    </div>
</div>
</template>

<script>
'use strict';

import { drawCat } from '../javascript/draw-cat';

export default {
    mounted() {
        drawCat('hsl(89, 100%, 55%)', 'black', this.$refs.catFace);
    },

    computed: {
        // Is the screen big enough to fit this cat head?
        prettyBigScreen: function() {
            return window.innerWidth > 500;
        }
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
    background-color: hsl(0, 0%, 16%);
    z-index: 100;
    padding: 2em;
}
.welcome-screen * {
    margin: 1em 0;
}

.content-wrapper {
    max-width: 750px;
    margin: auto;
}

em {
    color: hsl(89, 100%, 50%);
    font-style: normal;
}

.bottom-row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}
button {
    padding: 0.5em;
    height: 3em;
}

.footer {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    font-size: 0.75em;
}
.footer a {
    color: lightblue;
}
.footer a:visited {
    color: #b99bc8;
}
</style>
