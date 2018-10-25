<template>
  <nav class="navbar navbar-dark bg-primary p-0">
    <button class="navbar-toggler" type="button" @click="toggleSidebar()">
      <span class="sr-only">Toggle drawer</span>
      <i class="fa fa-bars"></i>
    </button>
    <ul class="nav navbar-nav">
      <li class="nav-item navbar-brand">Title</li>
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

<style>
</style>
