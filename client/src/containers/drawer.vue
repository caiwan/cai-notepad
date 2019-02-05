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
      </ul>
    </section>

    <!--- -->
    <hr />

    <section>
      <header class="navbar-sub">
        <a>Milestones</a>
      </header>
    </section>

    <!--- -->
    <hr />

    <section>
      <header class="navbar-sub">
        <a>Categories</a> [Edit]
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
          :maxDepth="0"
          v-on:itemAdded="addCategory"
          v-on:itemEdited="editCategory"
        />
        <li class="item list-group-item">
          <span
            class="add"
            v-if="!isAddingChild"
            @click="startAddChild"
          ><i class="fa fa-folder-plus"></i></span>

          <input
            autofocus
            autocomplete="off"
            placeholder="Category"
            class="add form-control"
            v-if="isAddingChild"
            v-model="newChild"
            v-focus="isAddingChild"
            @blur="doneAddChild"
            @keyup.enter="doneAddChild"
            @keyup.esc="cancelAddChild"
          />
        </li>
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
    ...mapActions('Categories', {
      addCategory: 'addNew',
      removeCategory: 'remove',
      editCategory: 'edit'
    }),
    ...mapMutations('UI', {
      toggleUI: 'toggle'
    }),

    toggleSidebar () {
      this.toggleUI('showSidebar');
    },

    startAddChild () {
      this.isAddingChild = true;
      this.newChild = '';
    },

    doneAddChild () {
      if (!this.isAddingChild) { return; }
      console.log({ parent: null, name: this.newChild });
      this.addCategory({ parent: null, name: this.newChild });
      this.isAddingChild = false;
      this.newChild = '';
    },

    cancelAddChild () {
      this.isAddingChild = false;
      this.newChild = '';
    }
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        el.focus();
      }
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
