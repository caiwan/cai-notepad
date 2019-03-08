<template>
  <div
    :style='styleObj'
    class='tree-container zebra'
  >
    <div
      class="node"
      :class='{"clicked": isClicked,"hover":isHover}'
    >
      <span :style="{ 'padding-left': (this.depth) * 22 + 'px' }">
      </span>
      <span class="icon">
        <span
          @click="toggle"
          :class="[isClicked ? 'clicked' : '', isFolder ? 'folder-icon' : 'folder-icon-placeholder']"
        ></span></span>
      <div
        v-if="!isEditing"
        :id='model.id'
        class='text-wrap'
        @click="toggle"
        @dblclick="doubleClick"
        @mouseover='mouseOver'
        @mouseout='mouseOut'
        :draggable='isDraggable'
        @drag.stop='drag'
        @dragstart.stop='dragStart'
        @dragover.stop='dragOver'
        @dragenter.stop='dragEnter'
        @dragleave.stop='dragLeave'
        @drop.stop='drop'
        @dragend.stop='dragEnd'
      >
        <span class='text'>{{model.name}}</span>
      </div>
      <div
        v-else
        class='text-wrap'
        @mouseover='mouseOver'
        @mouseout='mouseOut'
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
    </div>
    <div
      class='tree-margin'
      v-if="isFolder"
      v-show="open"
    >
      <drag-node
        v-for="item2 in model.children"
        :depth='increaseDepth'
        :model="item2"
        :key='item2.id'
        :disableDBClick='disableDBClick'
        :editingNode='editingNode'
      >
      </drag-node>
    </div>
  </div>
</template>

<script>
// vue-drag-tree

import { findRoot, exchangeData } from './drag-tree-util';
// let id = 1000;
let sourceNode = null;
let targetNode = null;
let nodeClicked = null;
let rootTree = null;
export default {
  name: 'DragNode',
  data () {
    return {
      open: false,
      isClicked: false,
      isHover: false,
      styleObj: {
        opacity: 1
      }
    };
  },

  props: {
    model: Object,
    allowDrag: {
      type: Function,
      default: () => true
    },
    allowDrop: {
      type: Function,
      default: () => true
    },
    depth: {
      type: Number,
      default: 0
    },
    disableDBClick: {
      type: Boolean,
      default: false
    },
    editingNode: {
      type: Object,
      default: null
    }
  },

  computed: {
    isFolder () { return 'children' in this.model && this.model.children.length; },
    increaseDepth () { return this.depth + 1; },
    isDraggable () { return this.allowDrag(this.model, this); },
    isEditing () { return this.editingNode === this.model; }
  },

  methods: {
    toggle () {
      if (this.isEditing) { return; }
      if (this.isFolder) {
        this.open = !this.open;
      }
      rootTree.nodeCurNodeClicked(this.model, this);
      this.isClicked = !this.isClicked;

      if (nodeClicked !== this.model.id) {
        let treeParent = rootTree.$parent;
        let nodeStack = [treeParent.$children[0]];
        while (nodeStack.length !== 0) {
          let item = nodeStack.shift();
          item.isClicked = false;
          if (item.$children && item.$children.length > 0) {
            nodeStack = nodeStack.concat(item.$children);
          }
        }
        this.isClicked = true;
        nodeClicked = this.model.id;
      }
    },
    startEdit (e) { rootTree.nodeStartEdit(this.model, this, e); },
    cancelEdit (e) { rootTree.nodeCancelEdit(this.model, this, e); },
    doneEdit (e) { rootTree.nodeDoneEdit(this.model, this, e); },
    mouseOver (e) { this.isHover = true; },
    mouseOut (e) { this.isHover = false; },
    doubleClick (e) { if (!this.disableDBClick && !this.isEditing) { this.startEdit(e); } },

    drag (e) {
      if (this.isEditing) { return; }
      sourceNode = this;
      rootTree.nodeDrag(this.model, this, e);
    },
    dragStart (e) {
      if (this.isEditing) { return; }
      e.dataTransfer.effectAllowed = 'move';
      // e.dataTransfer.setData('text/plain', 'asdad'); // LOL WUT?
      rootTree.nodeDragStart(this.model, this, e);
      return true;
    },
    dragOver (e) {
      if (this.isEditing) { return; }
      e.preventDefault();
      rootTree.nodeDragOver(this.model, this, e);
      return true;
    },
    dragEnter (e) {
      if (this.isEditing) { return; }
      if (this._uid !== sourceNode._uid) {
        this.styleObj.opacity = 0.5;
      }
      rootTree.nodeDragEnter(this.model, this, e);
    },
    dragLeave (e) {
      if (this.isEditing) { return; }
      this.styleObj.opacity = 1;
      rootTree.nodeDragLeave(this.model, this, e);
    },
    drop (e) {
      if (this.isEditing) { return; }
      e.preventDefault();
      this.styleObj.opacity = 1;
      if (!this.allowDrop(this.model, this)) {
        return;
      }
      targetNode = this;
      exchangeData(rootTree, sourceNode, targetNode);
      rootTree.nodeDrop({ sourceNode, targetNode }, this, e);
    },
    dragEnd (e) {
      if (this.isEditintig) { return; }
      rootTree.nodeDragEnd(this.model, this, e);
    }
  },

  updated () {
    rootTree.nodeUpdated();
  },

  created () {
    rootTree = findRoot(this);
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

.tree-container {
  .node {
    display: flex;
    align-items: baseline;
    // &.clicked {
    //   // background-color: $primary;
    // }
    // &.hover {
    // }
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
  &.zebra {
    &.even {
      background-color: $zebra-even-color;
    }
    &.odd {
      background-color: $zebra-odd-color;
    }
  }
}
</style>
