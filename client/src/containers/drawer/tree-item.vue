<template>

  <li>
    <span v-if="hasChildren" @click="toggleOpen">[{{ open ? 'v' : '>' }}]</span>
    <span class="item" v-if="!isEditing" :class="{folder: hasChildren}" @dblclick="startEdit">
      {{ model.name }}
    </span>
    <input class="edit" v-if="isEditing" v-model="model.name" v-focus="isEditing" @blur="doneEdit" @keyup.enter="doneEdit" @keyup.esc="cancelEdit" />

    <ul v-show="open" v-if="hasChildren">
      <tree-item class="item" v-for="(model, index) in model.children" :key="index" :model="model" />
      <li>
        <span class="add" v-if="!isAddingChild" @click="startAddChild">[+]</span>
        <input class="add" v-if="isAddingChild" v-model="newChild" v-focus="isAddingChild" @blur="doneAddChild" @keyup.enter="doneAddChild" @keyup.esc="cancelAddChild" />
      </li>
    </ul>
  </li>

</template>

<script>
import TreeItem from "./tree-item.vue"
export default {
  name: "TreeItem",
  components: {
    TreeItem
  },
  props: {
    model: Object
  },
  data() {
    return {
      open: false,
      isEditing: false,
      beforeEditCache: null,
      isAddingChild: false,
      newChild: ''
    }
  },
  computed: {
    hasChildren() {
      return this.model.children && this.model.children.length;
    }
  },
  methods: {
    toggleOpen() {
      this.open = !this.open
    },
    startEdit() {
      this.isEditing = true;
      this.beforeEditCache = this.model.name;
      // this.
    },
    doneEdit() {
      this.$emit('itemEdited', this.model);
      this.isEditing = false;
      this.beforeEditCache = null;
    },
    cancelEdit() {
      this.isEditing = false;
      this.model.name = this.beforeEditCache;
    },

    startAddChild() {
      this.isAddingChild = true;
    },
    doneAddChild() {
      this.$emit('itemAdded', this.model, this.newChild);
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
};

</script>

<style lang="scss" scoped>
</style>
