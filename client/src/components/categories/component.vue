<template>
  <div>
    <div class="treeSelf">
      <drag-tree
        :data="categories"
        :allowDrag="allowDrag"
        :allowDrop="allowDrop"
        :defaultText="'New Category'"
        @current-clicked="curNodeClicked"
        @drag="dragHandler"
        @drag-enter="dragEnterHandler"
        @drag-leave="dragLeaveHandler"
        @drag-over="dragOverHandler"
        @drag-end="dragEndHandler"
        @drop="dropHandler"
        @new="newHandler"
        @edit="editHandler"
        :disableDBClick="false"
        expand-all
      ></drag-tree>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
import DragTree from './drag-tree.vue';

export default {
  components: {
    DragTree
  },

  data () {
    return {
      isAddingChild: false,
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

    toggleSidebar () {
      this.toggleUI('showSidebar');
    },

    startAddChild () {
      this.isAddingChild = true;
      this.newChild = '';
    },

    doneAddChild () {
      if (!this.isAddingChild) { return; }
      // console.log({ parent: null, value: this.newChild });
      this.addCategory({ parent: null, value: this.newChild });
      this.isAddingChild = false;
      this.newChild = '';
    },

    cancelAddChild () {
      this.isAddingChild = false;
      this.newChild = '';
    },

    // -- Tree editor

    allowDrag (model, component) {
      return true;
    },
    allowDrop (model, component) {
      return true;
    },
    curNodeClicked (model, component) {
      // console.log("curNodeClicked", model, component);
    },
    dragHandler (model, component, e) {
      // console.log("dragHandler: ", model, component, e);
    },
    dragEnterHandler (model, component, e) {
      // console.log("dragEnterHandler: ", model, component, e);
    },
    dragLeaveHandler (model, component, e) {
      // console.log("dragLeaveHandler: ", model, component, e);
    },
    dragOverHandler (model, component, e) {
      // console.log("dragOverHandler: ", model, component, e);
    },
    dragEndHandler (model, component, e) {
      // console.log("dragEndHandler: ", model, component, e);
    },
    dropHandler (model, component, e) {
      // console.log("dropHandler: ", model, component, e);
    },
    newHandler (newItem) {
      this.addCategory({ parent: null, name: newItem });
    },
    editHandler (model, component, e) {
      console.log('Edit', { model, component, e });
      this.editCategory(model);
    }
  }

};
</script>

<style>
</style>
