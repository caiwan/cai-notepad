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
      </span>
      <span
        v-if="!isEditing"
        class="item"
        @dblclick="startEdit"
      >
        <router-link :to="{name: routerName, query:{category:model.id}}">
          {{ model.title }}
        </router-link>
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
        ><i class="fa fa-folder-plus"></i></span>
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
export default {
  name: 'CategoryItem',
  props: {
    model: Object,
    maxDepth: Number,
    lod: { default: 0, type: Number }
  },
  data () {
    return {
      open: false,
      isEditing: false,
      beforeEditCache: null,
      isAddingChild: false,
      newChild: '',
      routerName: this.$router.name
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
      console.log('lolz1');
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

<style lang="scss" scoped>
.item-group {
  display: flex;
  overflow: hidden;
  align-items: baseline;
}

ul {
  &.child {
    list-style: none;
    padding-left: 18pt;
    padding-top: 12px;

    li {
      padding: 6px 0px 6px 0px;
      position: relative;
      z-index: 2;
    }

    li::after {
      content: "";
      display: block;
      position: absolute;
      top: 0;
      right: -20px;
      bottom: 0;
      left: -32px;
      z-index: -1;
      user-select: none;
    }

    li:nth-child(odd)::after {
      background-color: rgba(255, 255, 255, 0.1);
    }
    li:nth-child(even)::after {
      background-color: rgba(0, 0, 0, 0.1);
    }
  }
}
</style>
