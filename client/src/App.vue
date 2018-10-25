<template>
  <div id="app" class="bmd-layout-container bmd-drawer-f-l" :class=" {'bmd-drawer-in' : showSidebar}">
    <header class="bmd-layout-header">
      <nav-bar />
    </header>
    <div class="bmd-layout-drawer navbar-dark bg-primary">
      <side-bar />
    </div>
    <main class="bmd-layout-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";

import NavBar from './containers/navbar.vue'
import SideBar from './containers/sidebar.vue'

export default {
  name: 'App',
  components: {
    NavBar, SideBar
  },
  computed: {
    ...mapState('UI', ['showSidebar'])
  }
}
</script>

<style lang="scss" rel="stylesheet/scss">
@import "scss/style.scss";
</style>
