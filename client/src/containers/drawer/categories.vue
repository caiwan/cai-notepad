<template>
  <!-- category tree -->
  <ul class="tree">
    <!-- TODO: v-for -->
    <tree-item v-if="categories.length" class="item" :model="categories" />
    <li>
      <span class="add" v-if="!isAddingChild" @click="startAddChild">[+]</span>
      <input class="add" v-if="isAddingChild" v-model="newChild" v-focus="isAddingChild" @blur="doneAddChild" @keyup.enter="doneAddChild" @keyup.esc="cancelAddChild" />
    </li>
  </ul>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
import TreeItem from './tree-item.vue'


export default {
  components: {
    TreeItem
  },
  data() {
    return {
      // treeData: testData
      isAddingChild: false,
      newChild: ''
    }
  },
  computed: {
    ...mapState("Categories", { categories: "items" })
  },
  created() {
    this.$store.dispatch("Categories/fetchAll");
  },
  methods: {
    ...mapActions("Categories", {
      addCategory: 'addNew',
      removeCategory: 'remove',
      // ... 
    }),

    startAddChild() {
      this.isAddingChild = true;
      this.newChild = '';
    },
    doneAddChild() {
      if (!this.isAddingChild)
        return;
      // this.$emit('itemAdded', this.model, this.newChild);
      console.log('lolz');
      this.addCategory({ parent: null, value: this.newChild });
      this.isAddingChild = false;
      this.newChild = '';
    },
    cancelAddChild() {
      this.isAddingChild = false;
      this.newChild = '';
    },
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        el.focus();
      }
    }
  }
}
</script>

<style>
</style>
