<template>
  <nav class="navbar navbar-dark">
    <a
      class="btn navbar-toggle"
      @click="toggleSidebar()"
    >
      <!-- <span>Toggle drawer</span> -->
      <i class="fa fa-bars"></i>
    </a>
    <input
      class="form-control"
      placeholder="Search"
    />

    <div class="btn-group dropdown">
      <div
        class="btn navbar-toggle"
        @click="toggleUserMenu()"
      >
        <i class="fa fa-user" />
        <ul
          class="dropdown-menu"
          v-if="showUserMenu"
        >
          <li>{{userName}}</li>
          <li><i class="fa fa-cog" />
            <router-link :to="{ name: 'User' }">Settings</router-link>
          </li>

          <li>
            <i class="fa fa-sign-out-alt" />
            <a
              href="#"
              @click="logout"
            >Logout</a></li>
        </ul>
      </div>
    </div>

  </nav>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

export default {
  computed: {
    ...mapState('UI', ['showUserMenu']),
    ...mapState('User', ['user']),
    userName () {
      return this.user ? this.user.display_name ? this.user.display_name : this.user.name : '';
    }
  },
  methods: {
    toggleSidebar () {
      this.$store.commit('UI/toggle', 'showSidebar');
    },
    toggleUserMenu () {
      this.$store.commit('UI/toggle', 'showUserMenu');
    },
    logout () {
      this.$store.dispatch('User/logout');
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../scss/_colors.scss";

nav {
  padding: 0px 6px !important;
  background-color: $primary !important;
  display: flex;
  flex-wrap: nowrap;
  word-break: keep-all;
  input {
    margin-left: 3px;
    padding-left: 3px;
    background-color: lighten($primary, 10) !important;
    color: $white !important;
    &::placeholder {
      color: $white !important;
      opacity: 0.5;
    }
    display: inline !important;
    flex-grow: 1;
  }
  .dropdown {
    .dropdown-toggle {
      word-break: keep-all;
    }
    .dropdown-menu {
      z-index: 10;
      position: absolute !important;
      display: block !important;
      left: -120px !important;
      width: 100px;
      padding: 8px;
    }
  }
}
</style>
