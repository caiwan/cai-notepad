<template>
  <section class='tree-node zebra'>

    <!-- TOGGLE ICON -->
    <span class="icon">
      <span
        @click="toggle"
        :class="[isOpen? 'clicked': '', isFolder ? 'folder-icon' : 'folder-icon-placeholder']"
      ></span></span>

    <!-- TITLE / EDIT -->
    <div
      v-if="!isEditing"
      :id='model.id'
      class='text-wrap'
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
        v-model="model.name"
        v-focus="isEditing"
        @blur="doneEdit"
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
        @click="mergeParent()"
      ><i class="fa fa-compress"></i></button>
    </template>
    <!-- Editing -->
    <template v-else>
      <!-- cancel / save -->
      <button
        class="btn btn-secondary input-grpup-append"
        @click="cancelEdit"
      ><i class=" fa fa-times"></i></button>
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
    };
  },

  computed: {
    isFolder () { return 'children' in this.model && this.model.children.length; },
    isOpen () { return this.model.open; },
    isEditing () { return this.editingNode === this.model; }
  },

  methods: {
    toggle () {},
    startEdit (e) { /* rootTree.nodeStartEdit(this.model, this, e); */ },
    cancelEdit (e) { /* rootTree.nodeCancelEdit(this.model, this, e); */ },
    doneEdit (e) { /* rootTree.nodeDoneEdit(this.model, this, e); */ },
    doubleClick (e) { if (/*! this.disableDBClick && */ !this.isEditing) { this.startEdit(e); } },
    mergeParent () { console.log('Hello'); }
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

$zebra-color-amount: 2.5;
$zebra-even-color: darken($secondary, 2 * $zebra-color-amount);
$zebra-odd-color: darken($secondary, $zebra-color-amount);

.tree-node {
  display: flex;
  align-items: baseline;
  .icon {
    height: auto; // usually 22x22
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
