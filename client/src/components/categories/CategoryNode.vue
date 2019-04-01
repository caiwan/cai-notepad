<template>
  <div
    class="tree-node"
    :class="[data.active ? store.activatedClass : '', data.open ? store.openedClass : '', data.class]"
    :id="data.id"
  >
    <section class='tree-container zebra'>
      <!-- TOGGLE ICON -->
      <span class="icon">
        <span
          @click="toggle"
          :class="[isClicked ? 'clicked' : '', isFolder ? 'folder-icon' : 'folder-icon-placeholder']"
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

    </section>

    <!-- <transition :name="store.nodesTransition"> -->
    <div
      class="tree-node-children"
      v-if="childrenVisible"
    >
      <TreeNode
        v-for="child in data.children"
        :key="child.id"
        :data="child"
        :store="store"
        :level="childrenLevel"
      ><template slot-scope="props">
          <slot
            :data="props.data"
            :store="props.store"
            :vm="props.vm"
          ></slot>
        </template></TreeNode>
    </div>
    <!-- </transition> -->
  </div>
</template>

<script>
import DraggableTreeNode from './dragtree/DraggableTreeNode';

export default {
  name: 'TreeNode',
  extends: DraggableTreeNode,

  computed: {
    isFolder () { return 'children' in this.model && this.model.children.length; },
    increaseDepth () { return this.depth + 1; },
    isDraggable () { return this.allowDrag(this.model, this); },
    isEditing () { return this.editingNode === this.model; }
  },

  methods: {
    toggle () {
      // if (this.isEditing) { return; }
      // if (this.isFolder) {
      //   this.open = !this.open;
      // }
      // rootTree.nodeCurNodeClicked(this.model, this);
      // this.isClicked = !this.isClicked;

      // if (nodeClicked !== this.model.id) {
      //   let treeParent = rootTree.$parent;
      //   let nodeStack = [treeParent.$children[0]];
      //   while (nodeStack.length !== 0) {
      //     let item = nodeStack.shift();
      //     item.isClicked = false;
      //     if (item.$children && item.$children.length > 0) {
      //       nodeStack = nodeStack.concat(item.$children);
      //     }
      //   }
      //   this.isClicked = true;
      //   nodeClicked = this.model.id;
      // }
    },
    startEdit (e) { /* rootTree.nodeStartEdit(this.model, this, e); */ },
    cancelEdit (e) { /* rootTree.nodeCancelEdit(this.model, this, e); */ },
    doneEdit (e) { /* rootTree.nodeDoneEdit(this.model, this, e); */ },
    // mouseOver (e) { this.isHover = true; },
    // mouseOut (e) { this.isHover = false; },
    doubleClick (e) { if (!this.disableDBClick && !this.isEditing) { this.startEdit(e); } }
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
