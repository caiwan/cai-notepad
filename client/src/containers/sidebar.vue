<template>
  <nav class="">
    <header class="navbar-brand">
      <a>Title</a>
    </header>

    <ul class="list-group">
      <li class="list-group-item">
        <a>Link 1</a>
      </li>
      <li class="list-group-item">
        <a>Link 2</a>
      </li>
      <li class="list-group-item">
        <a>Link 3</a>
      </li>
    </ul>

    <!--- -->
    <header class="navbar-brand">
      <a>Categories</a>
      [Edit]
    </header>

    <categories />
    <!--- -->

  </nav>
</template>

<script>

import Categories from './drawer/categories.vue'

export default {
  components: {
    Categories
  }
}
</script>

<style>
</style>
