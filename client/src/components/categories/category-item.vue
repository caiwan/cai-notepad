<template>
  <li v-if="!maxDepth || lod<maxDepth">
    <span class="item-group">
      <span
        v-if="!maxDepth || lod+1<maxDepth"
        @click="toggleOpen"
      >
        <i
          class="fa"
          :class="open ? 'fa-caret-down' : 'fa-caret-right' "
        >&nbsp;</i>
        [{{open ? 'close' : 'open' }}]
      </span>
      <span>[Delete]</span>
      <span
        v-if="!isEditing"
        class="item"
        @dblclick="startEdit"
      >
        {{ model.title }}
      </span>
      <input
        class="edit form-control"
        v-if="isEditing"
        v-model="model.title"
        v-focus="isEditing"
        @blur="cancelEdit"
        @keyup.enter="doneEdit"
        @keyup.esc="cancelEdit"
      />
    </span>
    <ul
      v-if="open"
      class="child"
    >
      <category-item
        class="item"
        v-for="(model, index) in model.children"
        :key="index"
        :model="model"
        :maxDepth="maxDepth"
        :lod="lod+1"
        v-on:itemAdded="itemAdded"
        v-on:itemEdited="itemEdited"
      />
      <li>
        <span
          class="add"
          v-if="!isAddingChild"
          @click="startAddChild"
        ><i class="fa fa-folder-plus"></i>New child</span>
        <input
          autofocus
          autocomplete="off"
          placeholder="Category"
          class="add form-control"
          v-if="isAddingChild"
          v-model="newChild"
          v-focus="isAddingChild"
          @blur="cancelAddChild"
          @keyup.enter="doneAddChild"
          @keyup.esc="cancelAddChild"
        />
      </li>
    </ul>
  </li>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
export default {
  name: 'CategoryItem',

  props: {
    model: Object,
    maxDepth: { default: 0, type: Number },
    lod: { default: 0, type: Number }
  },

  data () {
    return {
      open: false,
      isEditing: false,
      beforeEditCache: null,
      isAddingChild: false,
      newChild: ''
    };
  },

  computed: {
  },

  methods: {
    toggleOpen () {
      this.open = !this.open;
    },
    startEdit () {
      this.isEditing = true;
      this.beforeEditCache = this.model.title;
    },
    doneEdit () {
      if (!this.isEditing) { return; }
      this.$emit('itemEdited', this.model);
      this.isEditing = false;
      this.beforeEditCache = null;
    },
    cancelEdit () {
      if (!this.isEditing) { return; }
      this.isEditing = false;
      this.model.title = this.beforeEditCache;
    },

    startAddChild () {
      this.isAddingChild = true;
    },
    doneAddChild () {
      this.$emit('itemAdded', { parent: this.model, value: this.newChild });
      this.isAddingChild = false;
      this.newChild = '';
    },
    cancelAddChild () {
      this.isAddingChild = false;
      this.newChild = '';
    },
    itemAdded (parent, newChild) {
      this.$emit('itemAdded', { parent: parent, value: newChild });
    },
    itemEdited (model) {
      this.$emit('itemEdited', model);
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

<style>
</style>
