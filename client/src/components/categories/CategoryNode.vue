<template>
  <section class='tree-node zebra'>

    <!-- TOGGLE ICON -->
    <span
      class="icon"
      @click="toggle"
    >
      <span :class="[isOpen? 'clicked': '', isFolder ? 'folder-icon' : 'folder-icon-placeholder']"></span></span>

    <!-- TITLE / EDIT -->
    <div
      v-if="!isEditing"
      :id='model.id'
      class='text-wrap'
      @click="toggle"
      @dblclick="doubleClick"
    >
      <span class='text'>{{model.name}}</span>
    </div>
    <div
      v-else
      class='text-wrap'
    >
      <input
        autocomplete="off"
        placeholder="Category"
        class="form-control edit input-group-prepend"
        v-model="editingItem.name"
        v-focus="isEditing"
        @keyup.enter="doneEdit"
        @keyup.esc="cancelEdit"
      />
    </div>

    <!-- Browse -->
    <template v-if="!isEditing">
      <!-- Edit mode -->
      <button
        class="btn btn-primary input-grpup-append"
        @click="startEdit"
      ><i class="fa fa-edit"></i></button>
      <!-- Merge up -->
      <button
        class="btn btn-danger input-grpup-append"
        @click="remove()"
      ><i class="fa fa-trash"></i></button>
    </template>
    <!-- Editing -->
    <template v-else>
      <!-- cancel / save -->
      <button
        class="btn btn-secondary input-grpup-append"
        @click="cancelEdit"
      ><i class="fa fa-times"></i></button>
      <button
        class="btn btn-success input-grpup-append"
        @click="doneEdit"
      ><i class="fa fa-check"></i></button>
    </template>
  </section>
</template>

<script>

export default {
  name: 'Category',

  props: {
    model: { type: Object, required: true },
    treeControl: { type: Object, required: true }
  },

  data () {
    return {
      editingItem: null
    };
  },

  computed: {
    isFolder () { return 'children' in this.model && this.model.children.length; },
    isOpen () { return this.model.open; },
    isEditing () { return this.editingItem !== null; }
  },

  methods: {
    toggle () { this.treeControl.toggleOpen(this.model); },
    startEdit (e) {
      const { id, name } = this.model;
      this.editingItem = { id, name };
    },
    cancelEdit (e) { this.editingItem = null; },
    doneEdit (e) {
      const { id, name } = this.editingItem;
      const editedItem = { id, name };
      this.$emit('edited', editedItem); this.editingItem = null;
      this.model = Object.assign(this.model, editedItem);
    },
    doubleClick (e) { if (!this.isEditing) { this.startEdit(e); } },
    remove () { this.$emit('remove', this.model); this.editingItem = null; }
  },

  updated () {
    // rootTree.nodeUpdated();
  },

  created () {
    // rootTree = findRoot(this);
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) { setTimeout(() => { el.focus(); }, 0); }
    }
  }

};
</script>

<style lang="scss" scoped>
@import "@/scss/_colors.scss";

$zebra-color-amount: 4.5;
$zebra-even-color: darken($secondary, $zebra-color-amount);
$zebra-odd-color: lighten($secondary, $zebra-color-amount);

.tree-node {
  display: flex;
  align-items: baseline;
  .icon {
    height: 100%; // usually 22x22
    width: auto;
    .folder-icon {
      display: inline-block;
      margin-left: 10px;
      margin-right: 8px;
      border-left: 4px solid grey;
      border-top: 4px solid transparent;
      border-bottom: 4px solid transparent;
      border-right: 0 solid yellow;
      transition: transform 0.3s ease-in-out;
      &.clicked {
        transform: rotate(90deg);
      }
    }
    .folder-icon-placeholder {
      margin-left: 22px;
    }
  }
  .text {
    flex-grow: 1;
  }
  .edit {
    flex-grow: 1;
  }

  .text-wrap {
    flex-grow: 1;
    display: flex;
    align-items: baseline;

    padding-left: 8px;
    cursor: pointer;
  }
}
</style>
