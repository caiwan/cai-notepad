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
        :data="originalData"
        draggable
        crossTree
        ref="tree1"
        @change="treeChange"
        @drag="ondrag"
        @drop="ondrop"
      />
    </section>

  </div>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
import zebrafy from '@/utils/zebrafy';

import BaseTree from './dragtree/DraggableTree';
import CategoryTreeNode from './CategoryNode.vue';

export default {
  components: {
    'Tree': {
      extends: BaseTree,
      components: {
        TreeNode: CategoryTreeNode
      }
    }
  },

  data () {
    return {};
  },

  computed: {
    ...mapState('Categories', {
      categories: 'itemTree'
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
      this.data = targetTree.getPureData();
    },
    ondrag () {
      const tree = this.$refs.tree1;
      tree.nodesTransition = null;
    },
    ondrop () {
      const tree = this.$refs.tree1;
      tree.nodesTransition = 'fade';
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
@import "@/scss/__category_selector.scss";
</style>
