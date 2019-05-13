<template>
  <li
    class="selector-item zebra"
    v-if="!maxDepth || lod<maxDepth"
    :class="{selected: model === selected}"
  >
    <span
      :class="{folder: hasChildren}"
      @click="select(model)"
    >
      {{ model.name }}
    </span>
    <ul
      class="selector-group"
      v-if="hasChildren"
    >
      <category-item
        class="item"
        v-for="(item, index) in model.children"
        :key="index"
        :model="item"
        :maxDepth="maxDepth"
        v-on:itemSelected="select(item)"
        :lod="lod+1"
        :selected="selected"
      />
    </ul>
  </li>
</template>

<script>
// import CategoryItem from "./category-item.vue"
export default {
  name: 'CategoryItem',
  // components: {
  // CategoryItem
  // },
  props: {
    model: Object,
    maxDepth: Number,
    lod: { default: 0, type: Number },
    selected: { type: Object, default: null }

  },
  data () {
    return {
      open: false,
      isEditing: false,
      beforeEditCache: null,
      isAddingChild: false,
      newChild: ''
    };
  },
  computed: {
    hasChildren () {
      return this.model.children && this.model.children.length;
    }
  },
  methods: {
    select (item) {
      this.$emit('itemSelected', item);
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../scss/__category_selector.scss";
</style>
