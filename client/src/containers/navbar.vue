<template>
  <nav class="navbar navbar-dark">
    <a
      class="btn navbar-toggler"
      @click="toggleSidebar()"
    >
      <!-- <span>Toggle drawer</span> -->
      <i class="fa fa-bars"></i>
    </a>
    <input
      class="form-control"
      placeholder="Search"
    />
    <ul class="nav navbar-nav px-3">
      <li class="nav-item navbar-brand">Notes</li>
    </ul>
  </nav>
</template>

<script>

export default {
  methods: {
    toggleSidebar() {
      this.$store.commit("UI/toggle", 'showSidebar');
    }
  }
}
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
}
</style>
