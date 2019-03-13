<template>
  <section class="container-flex">
    <div class="col-md-12 tree-self">

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

      <!-- List and edit the current ones -->

      <template>
        <div
          ref="placeholder"
          id="category-drag-placeholder"
          class="placeholder"
          v-show="isDragging"
        ></div>
        <template v-for='(item,index) in newData'>
          <drag-node
            :model='item'
            :depth='0'
            :defaultText='defaultText'
            :key='index'
            :editingNode="editingCategory"
          ></drag-node>
        </template>
      </template>

    </div>
  </section>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

import DragNode from './drag-node.vue';
import zebrafy from '@/utils/zebrafy';
export default {
  name: 'DragTree',
  components: {
    DragNode
  },

  data () {
    return {
      // RM these later on:
      allowDrag: () => true,
      allowDrop: () => true,
      depth: 0,
      disableDBClick: false,
      defaultText: 'New category',

      items: {},
      newChild: '',

      isDragging: false
    };
  },
  computed: {
    ...mapState('Categories', {
      categories: 'itemTree',
      editingCategory: 'editingItem'
    }),
    newData: {
      get () {
        return this.categories;
      },
      set (newValue) {
        //
        console.log('Hello', newValue);
        let length = this.categories.length;
        for (let i = 0; i < length; i++) {
          this.categories.shift(i);
        }
        // this.categories = Object.assign(this.categories, newValue);
      }
    }
  },
  methods: {
    ...mapActions('Categories', {
      addCategory: 'addNew',
      removeCategory: 'remove',
      editCategory: 'edit',
      startEditCategory: 'startEdit',
      cancelEditCategory: 'cancelEdit',
      doneEditCategory: 'doneEdit',
      moveCategory: 'move'
    }),

    nodeCurNodeClicked (model, component) {
      // console.log('[1]', { model, component });
    },
    nodeDrag (model, component, e) {
      // console.log('[DragStart]', { model, component });
      // this.isDragging = true;
    },

    nodeDragStart (model, component, e) {
      console.log('[DragStart]', { model, component });
      this.isDragging = true;
    },
    nodeDragEnd (model, component, e) {
      console.log('[DragEnd]', { model, component });
      this.isDragging = true;
    },

    nodeDragEnter (model, component, e) {
      // console.log('[3]', { model, component });
    },
    nodeDragLeave (model, component, e) {
      // console.log('[4]', { model, component });
    },
    nodeDragOver (model, component, e) {
      // console.log('[5]', { model, component });
    },
    nodeDrop ({ sourceNode, targetNode }, component, e) {
      let newParent = null;
      let item = sourceNode.model;
      if (targetNode !== this || targetNode.$options._componentTag === 'drag-node') {
        newParent = targetNode.model;
      }
      console.log('[Drop]', { item, newParent, component, e });
      this.moveCategory({ item, newParent, newOrder: item.order - 1 });
    },

    nodeStartEdit (model, component, e) {
      console.log('[8]', { model, component });
      this.startEditCategory(model);
    },
    nodeDoneEdit (model, component, e) {
      console.log('[9]', { model, component, e });
      this.doneEditCategory(model);
    },
    nodeCancelEdit (model, component, e) {
      console.log('[A]', { model, component, e });
      this.cancelEditCategory(model);
    },

    nodeUpdated () {
      let el = this.$el;
      setTimeout(() => { zebrafy(el); }, 0);
    },

    nodeMovePlaceholder (component) {
      // Move placeholder tag to somewhere else
    },

    doneAddChild () {
      console.log('Hello', { parent: null, name: this.newChild, a: this.addCategory });
      this.addCategory({ parent: null, name: this.newChild });
      this.newChild = '';
    },
    cancelAddChild () {
      this.newChild = '';
    }

  },

  updated () {
    let el = this.$el;
    setTimeout(() => { zebrafy(el); }, 0);
  },

  created () {
    let self = this;
    setTimeout(() => { zebrafy(self.$el); }, 0);
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
@import "@/scss/_colors.scss";
@import "@/scss/__category_selector.scss";

.placeholder {
  background-color: $secondary;
  // width: 100;
}
</style>
