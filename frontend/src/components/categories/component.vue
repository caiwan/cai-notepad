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
        class="tree"
        @change="treeChange"
        @drag="ondrag"
        @nodeOpenChanged="zebra()"
        @drop="zebra()"
      ><template slot-scope="{ data, store }">
          <category
            :model="data"
            :treeControl="store"
            @edited="editCategory"
            @remove="removeCategory"
          /> </template>
      </Tree>
    </section>

  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import * as th from 'tree-helper';

import zebrafy from '@/utils/zebrafy';

import Tree from '@/containers/dragtree/DraggableTree';
import Category from './CategoryNode.vue';

export default {
  components: {
    Tree, Category
  },

  data () {
    return {
      newChild: '',
      categories: []
    };
  },

  computed: {
    ...mapState('Categories', {
      categoryTree: 'itemTree'
    }),
    ...mapGetters('Categories', {
      category: 'category'
    })
  },

  methods: {
    ...mapActions('Categories', {
      addCategory: 'addNew',
      // removeCategory: 'remove',
      editCategory: 'edit',
      moveCategory: 'move'
    }),

    treeChange (node, targetTree) {
      const item = Object.assign({}, this.category(node.id));
      const index = node.parent.children.indexOf(node);
      const parentId = node.parent.id || null;
      this.moveCategory({ item, index, parentId });
    },

    ondrag (node) {
      // Trinm max level
      const MAX_LEVEL = 3;
      if (MAX_LEVEL) {
        let nodeLevels = 1;
        th.depthFirstSearch(node, (childNode) => {
          if (childNode._vm.level > nodeLevels) { nodeLevels = childNode._vm.level; }
        });
        nodeLevels = nodeLevels - node._vm.level + 1;
        const childNodeMaxLevel = MAX_LEVEL - nodeLevels;
        //
        th.depthFirstSearch(this.categories, (childNode) => {
          if (childNode === node) { return; }
          if (!childNode._vm) { console.warn(childNode); }
          this.$set(childNode, 'droppable', childNode._vm.level <= childNodeMaxLevel);
        });
      }
    },

    zebra () {
      let self = this;
      setTimeout(() => { zebrafy(self.$el); });
    },

    refreshView () {
      let self = this;
      setTimeout(() => {
        self.categories = JSON.parse(JSON.stringify(self.categoryTree));
        zebrafy(self.$el);
      });
    },

    cancelAddChild () {
      this.newChild = '';
    },

    doneAddChild () {
      this.addCategory({ parent: null, name: this.newChild });
      this.newChild = '';
    },

    removeCategory (category) {
      if (confirm('Deleting a category will merge everything assigned to it to its parent. However it cannnot be undone. Are you sure?')) {
        this.$store.dispatch('Categories/remove', category);
      }
    }

  },

  updated () {
    this.zebra();
  },

  created () {
    this.refreshView();
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        setTimeout(() => { el.focus(); }, 0);
      }
    }
  },

  watch: {
    categoryTree () {
      this.refreshView();
    }
  }

};
</script>

<style lang="scss" scoped>
@import "@/scss/__category_selector.scss";
@import "@/scss/_colors.scss";
.tree {
  margin: 0 4px;

  .zebra {
    &.even {
      background-color: $zebra-even-color;
    }
    &.odd {
      background-color: $zebra-odd-color;
    }
  }
}
</style>
