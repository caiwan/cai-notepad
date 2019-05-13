<template>
  <li v-if="!maxDepth || lod<maxDepth">
    <span class="item-group">
      <span
        class="folder"
        v-if="!maxDepth || lod+1<maxDepth && isFolder"
        @click="toggle"
      >
        <i
          class="fa"
          :class="open ? 'fa-caret-down' : 'fa-caret-right' "
        >&nbsp;</i>
      </span>
      <span class="item">
        <router-link :to="{name: routerName, query:{category:model.id}}">
          {{ model.name }}
        </router-link>
      </span>
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
      />
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
      routerName: this.$router.name
    };
  },
  computed: {
    isFolder () { return this.model.children && this.model.children.length; }
  },
  methods: {
    toggle () {
      this.open = !this.open;
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
.folder {
  width: 24px;
  height: 24px;
  i {
    padding-left: 6px;
  }
}

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
