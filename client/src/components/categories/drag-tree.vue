<template>
  <div>
    <template v-for='(item,index) in newData'>
      <drag-node
        :model='item'
        :allowDrag='allowDrag'
        :allowDrop='allowDrop'
        :depth='increaseDepth'
        :defaultText='defaultText'
        :disableDBClick='disableDBClick'
        :key='index'
      ></drag-node>
    </template>
    <div class="dnd-container zebra ">
      <template v-if="!isAddingChild">
        <span
          class="add"
          @click="startAddChild"
        >
          + Add new
        </span>
      </template>
      <template v-else>
        <input
          autocomplete="off"
          placeholder="Category"
          class="add"
          v-model="newChild"
          v-focus="isAddingChild"
          @blur="doneAddChild"
          @keyup.enter="doneAddChild"
          @keyup.esc="cancelAddChild"
        />
      </template>
    </div>

  </div>
</template>

<script>
import DragNode from './drag-node.vue';
import zebrafy from '@/utils/zebrafy';
export default {
  name: 'DragTree',
  components: {
    DragNode
  },
  props: {
    data: Array,
    allowDrag: {
      type: Function,
      default: () => true
    },
    allowDrop: {
      type: Function,
      default: () => true
    },
    defaultText: {
      //
      type: String,
      default: 'New Node'
    },
    depth: {
      type: Number,
      default: 0
    },
    disableDBClick: { // item
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      items: {},
      isAddingChild: false,
      newChild: ''
    };
  },
  computed: {
    increaseDepth () {
      return this.depth + 1;
    },
    newData: {
      // getter
      get () {
        return this.data;
      },
      // setter
      set (newValue) {
        //
        let length = this.data.length;
        for (let i = 0; i < length; i++) {
          this.data.shift(i);
        }
        // target
        this.data = Object.assign(this.data, newValue);
      }
    }
  },
  methods: {
    emitCurNodeClicked (model, component) {
      this.$emit('current-node-clicked', model, component);
    },
    emitDrag (model, component, e) {
      this.$emit('drag', model, component, e);
    },
    emitDragEnter (model, component, e) {
      this.$emit('drag-enter', model, component, e);
    },
    emitDragLeave (model, component, e) {
      this.$emit('drag-leave', model, component, e);
    },
    emitDragOver (model, component, e) {
      this.$emit('drag-over', model, component, e);
    },
    emitDragEnd (model, component, e) {
      this.$emit('drag-end', model, component, e);
    },
    emitDrop (model, component, e) {
      this.$emit('drop', model, component, e);
    },
    nodeUpdated () {
      zebrafy(this.$el);
    },

    startAddChild () {
      this.isAddingChild = true;
    },
    doneAddChild () {
      if (!this.isAddingChild) return;
      this.$emit('new', this.newChild);
      this.isAddingChild = false;
      this.newChild = '';
    },
    cancelAddChild () {
      this.isAddingChild = false;
      this.newChild = '';
    },
    emitEdit (model, component, e) {
      this.$emit('edit', model, component, e);
    }
  },
  updated () {
    zebrafy(this.$el);
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

// <style lang="scss">
// $zebra-even-color: white;
// $zebra-odd-color: #f6f6f6;

//
</style>
