<template>
  <div id="app">
    <div
      id="spinner"
      :class="{visible: isLoading}"
    ></div>

    <template v-if="isLoggedIn">
      <header
        id="header"
        class="top-nav drawer-transition"
        :class="{'drawer-on' : showSidebar}"
      >
        <nav-bar v-if="!isInitializing" />
      </header>

      <div
        id="drawer"
        :class="{'drawer-on' : showSidebar}"
      >
        <drawer v-if="!isInitializing" />
      </div>
    </template>

    <main
      id="main"
      class="drawer-transition"
      :class="{'drawer-on' : showSidebar}"
    >
      <router-view v-if="!isInitializing" />
    </main>

    <footer
      id="footer"
      class="drawer-transition"
      :class="{'drawer-on' : showSidebar}"
    >
      <div
        id="snackbar"
        :class="{'snackbar-on' : showSnackbar}"
        @click="dismissSnackbar"
      >
        <ul>
          <li
            v-for="(message, index) in snackbarMessages"
            :key="index"
          >{{message}}</li>
        </ul>
      </div>
    </footer>

  </div>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

import NavBar from './containers/navbar.vue';
import Drawer from './containers/drawer.vue';

import io from './services/io';

export default {
  name: 'App',
  components: {
    NavBar, Drawer
  },
  computed: {
    ...mapState('UI', ['showSidebar', 'showSnackbar', 'snackbarMessages']),
    ...mapGetters('UI', ['isLoading']),
    ...mapGetters('User', ['isLoggedIn']),
    ...mapState('App', ['isInitializing'])
  },
  methods: {
    ...mapActions('User', ['fetchProfile']),
    ...mapMutations('App', ['initialized']),
    dismissSnackbar () {
      this.$store.commit('UI/pullSnackbar');
      console.log('dismiss');
    }
  },
  async created () {
    await io.initialized;
    this.fetchProfile();
    this.initialized();
  }
};
</script>

<style lang="scss" rel="stylesheet/scss">
@import "@/scss/style.scss";

$transition-speed: 0.5s;
$drawer-width: 250px;

#drawer {
  height: 100%;
  width: $drawer-width;
  position: fixed;
  word-break: keep-all;
  z-index: 10;
  top: 0;
  left: -$drawer-width;
  background-color: $primary;
  overflow-x: hidden;
  transition: $transition-speed;

  &.drawer-on {
    left: 0px;
    width: $drawer-width !important;
  }
}

#footer {
  position: fixed;
  // width: 100%;
  left: 15px;
  right: 15px;
  bottom: 0px;

  &.drawer-on {
    // left: $drawer-width !important;
  }

  #snackbar {
    position: relative;
    bottom: 30px;
    visibility: hidden;
    // min-width: 250px;
    // width: auto;
    margin: 0 auto;
    background-color: $warning;
    color: $gray-800;
    text-align: center;
    border-radius: 4px;
    padding: 16px;
    z-index: 20;

    @keyframes fadein {
      from {
        bottom: 0;
        opacity: 0;
      }
      to {
        bottom: 30px;
        opacity: 1;
      }
    }
    @keyframes fadeout {
      from {
        bottom: 30px;
        opacity: 1;
      }
      to {
        bottom: 0;
        opacity: 0;
      }
    }

    &.snackbar-on {
      visibility: visible !important;
      // animation: fadein 0.5s, fadeout 0.5s 2.5s;
      animation: fadein 0.5s;
    }

    ul {
      margin: 0px;
      padding: 0px;
      list-style-type: none;
      li {
        padding: 0px;
        margin: 0.5em 0em 0.5em 0em;
      }
    }
  }
}

#spinner {
  position: fixed;
  visibility: hidden;
  z-index: 60;

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  &::after {
    content: "";
    position: fixed;
    width: 96px;
    height: 96px;
    top: calc(50% - 48px);
    left: calc(50% - 48px);
    border-radius: 50%;
    border: 8px solid $cyan;
    border-left-color: transparent;
    animation: spin 2s infinite linear;
  }

  &.visible {
    visibility: visible;
  }
}

#header {
  &.top-nav {
    transition: $transition-speed;
    margin-left: 0px;
  }
}

.drawer-transition {
  transition: $transition-speed;
  &.drawer-on {
    // desktop
    margin-left: 0px;

    //mobile
    @include respond-to(md) {
      margin-left: $drawer-width !important;
    }
  }
}
</style>
