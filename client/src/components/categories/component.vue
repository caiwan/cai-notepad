<template>
  <div>
    <!-- Add new category -->
    <header class="card card bg-light mx-1 my-2">
      <div class="card-body py-2">
        <div class="input-group">
          <div class="btn btn-secondary input-group-prepend">
            <i class="fa fa-folder-plus"></i>
          </div>
          <input
            class="form-control input-group-append"
            autofocus
            autocomplete="off"
            placeholder="Add Category"
            v-model="newChild"
            @blur="cancelAddChild()"
            @keyup.enter="doneAddChild()"
            @keyup.esc="cancelAddChild()"
          />

          <button
            class="btn btn-success input-group-append"
            @click="doneAddChild()"
          ><i class="fa fa-plus"></i></button>
        </div>
      </div>
    </header>

    <section>
      <Tree
        :data="categories"
        draggable
        crossTree
        ref="category-editor"
        @change="treeChange"
        @drag="ondrag"
        @drop="ondrop"
      ><template slot-scope="{ data, store }">
          <category
            :model="data"
            :treeControl="store"
          /> </template>
      </Tree>
    </section>

  </div>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
import * as hp from 'helper-js';
import * as th from 'tree-helper';

import zebrafy from '@/utils/zebrafy';

import Tree from './dragtree/DraggableTree';
import Category from './CategoryNode.vue';

export default {
  components: {
    Tree, Category
  },

  data () {
    return {
      newChild: '',
      categories: null
    };
  },

  computed: {
    ...mapState('Categories', {
      storedCategories: 'itemTree'
    })
  },

  methods: {
    ...mapActions('Categories', {
      addCategory: 'addNew',
      removeCategory: 'remove',
      editCategory: 'edit',
      startEditCategory: 'startEdit',
      cancelEditCategory: 'cancelEdit',
      doneEditCategory: 'doneEdit'
    }),
    treeChange (node, targetTree) {
      // const data = targetTree.getPureData();
    },
    ondrag (node) {
      const MAX_LEVEL = 0; // 3 == 2
      if (MAX_LEVEL) {
        // const {maxLevel} = this
        let nodeLevels = 1;
        th.depthFirstSearch(node, (childNode) => {
          if (childNode._vm.level > nodeLevels) {
            nodeLevels = childNode._vm.level;
          }
        });
        nodeLevels = nodeLevels - node._vm.level + 1;
        const childNodeMaxLevel = MAX_LEVEL - nodeLevels;
        //
        th.depthFirstSearch(this.originalData, (childNode) => {
          if (childNode === node) {
            return;
          }
          if (!childNode._vm) {
            console.warn(childNode);
          }
          this.$set(childNode, 'droppable', childNode._vm.level <= childNodeMaxLevel);
        });
      }

      const tree = this.$refs.tree1;
      tree.nodesTransition = null;
    },

    ondrop () {
    },

    cancelAddChild () {
      this.newChild = '';
      // this.categories = Object.assign({}, this.storedCategories);
    },
    doneAddChild () {
      // ... + store add func
      this.newChild = '';
      // this.categories = Object.assign({}, this.storedCategories);
    }

  },

  updated () {
    let el = this.$el;
    setTimeout(() => { zebrafy(el); });
  },

  created () {
    this.$store.dispatch('Categories/clear');
    this.$store.dispatch('Categories/fetchAll');

    console.log('ugromokus', { s: this.storedCategories });

    this.categories = Object.assign([], this.storedCategories);

    console.log('Hapci', { s: this.storedCategories, c: this.categories });

    let self = this;
    setTimeout(() => { zebrafy(self.$el); });
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        setTimeout(() => { el.focus(); }, 0);
      }
    }
  }

};
</script>

<style lang="scss" scoped>
@import "@/scss/__category_selector.scss";
@import "@/scss/_colors.scss";

.zebra {
  &.even {
    background-color: $zebra-even-color;
  }
  &.odd {
    background-color: $zebra-odd-color;
  }
}
</style>
