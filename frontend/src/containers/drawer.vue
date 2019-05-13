<template>
  <nav>
    <header class="navbar-brand">
      <a>Notes</a>
      <span
        class="close"
        @click="toggleSidebar()"
      >&times;</span>
    </header>

    <section>
      <ul class="list-group">
        <li class="list-group-item">
          <router-link :to="{ name: 'Dashboard' }"><i class="fa fa-columns"></i>Dashboard</router-link>
        </li>
        <li class="list-group-item">
          <router-link :to="{ name: 'Notes' }"><i class="fa fa-sticky-note"></i>Notes</router-link>
        </li>
        <li class="list-group-item">
          <router-link :to="{ name: 'Tasks' }"><i class="fa fa-tasks"></i>Tasks</router-link>
        </li>
        <!-- <li class="list-group-item">
          <router-link :to="{ name: 'Categories' }"><i class="fa fa-folder"></i>Categories</router-link>
        </li> -->
      </ul>
    </section>

    <!--- -->
    <hr />

    <section>
      <header class="navbar-sub">
        Milestones [Edit]
      </header>
    </section>

    <!--- -->
    <hr />

    <section>
      <header class="navbar-sub">
        Categories
        [<router-link :to="{name: 'Categories'}">Edit</router-link>]
      </header>
      <!-- category tree -->
      <ul class="tree list-group">
        <li class="item list-group-item">
          <router-link :to="{name: routerName, query:{category:'all'}}">All</router-link>
        </li>

        <li class="item list-group-item">
          <router-link :to="{name: routerName, query:{category:'unassigned'}}">Unassigned</router-link>
        </li>
        <category-item
          v-for="(category, index) in categories"
          :key="index"
          class="item list-group-item"
          :model="category"
          :maxDepth="2"
        />

      </ul>
    </section>

    <!--- -->
    <hr />

    <header class="navbar-sub">
      <a>Tags</a>
    </header>

  </nav>
</template>

<script>

import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
import CategoryItem from './category-drawer-item.vue';

export default {
  components: {
    CategoryItem
  },

  data () {
    return {
      isAddingChild: false,
      routerName: this.$router.name,
      newChild: ''
    };
  },

  computed: {
    ...mapState('Categories', { categories: 'itemTree' })
  },

  created () {
    this.$store.dispatch('Categories/fetchAll');
  },

  methods: {
    ...mapMutations('UI', {
      toggleUI: 'toggle'
    }),

    toggleSidebar () {
      this.toggleUI('showSidebar');
    }

  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) { setTimeout(() => { el.focus(); }, 0); }
    }
  }

};

</script>

<style lang="scss" scoped>
@import "../scss/_colors.scss";
@import "../scss/_mixins.scss";

nav {
  padding: 0 4px;
  header {
    .close {
      visibility: show;
      position: absolute;
      top: 0;
      right: 25px;
      font-size: 36px;
      margin-left: 50px;
      @include respond-to(md) {
        visibility: hidden;
      }
    }
  }

  .list-group {
    padding: 2px 4px 2px 4px;
    .list-group-item {
      background-color: darken($primary, 10) !important;
      border-color: lighten($primary, 20);
      padding-left: 8px;
      i {
        &.fa {
          margin-right: 8px;
        }
      }
    }
    .tree {
      margin: 0px;
    }
  }
  hr {
    border-color: lighten($primary, 20);
  }
}
</style>
