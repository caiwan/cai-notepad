import io from '@/services/io';
import common from '@/store/_common';

export default {
  namespaced: true,

  state: {
    items: [],
    itemMap: [],
    itemTree: [],
    isLoaded: false
  },

  getters: {
    category: (state) => (id) => (id in state.itemMap ? state.itemMap[id] : null),
    categoryName: (state) => (id) => (id in state.itemMap ? state.itemMap[id].name : 'Unassigned')
  },

  mutations: {
    clear: (state) => {
      state.items = [];
      state.itemMap = [];
      state.itemTree = [];
      state.isLoaded = false;
    },
    put: (state, item) => {
      if (!item.hasOwnProperty('children')) {
        item['children'] = [];
      }
      state.itemMap[item.id] = item;
      if (item.parent) {
        if (!state.itemMap[item.parent]) { state.itemMap[item.parent] = { children: [] }; };
        state.itemMap[item.parent].children.push(state.itemMap[item.id]);
      } else {
        state.itemTree.push(state.itemMap[item.id]);
      }
      state.items.push(item);
    },

    edit: (state, item) => {
      let storedItem = state.itemMap[item.id];
      for (let key in item) {
        if (item.hasOwnProperty(key)) {
          storedItem[key] = item[key];
        }
      }
    },

    reorder: (state, { item, oldParentId, oldOrder }) => {
      const editedItem = state.itemMap[item.id];
      // find the parent where the item was
      const oldParent = !oldParentId ? state.itemTree : state.itemMap[oldParentId].children;
      // find the parent where the item is supposed to be
      const newParent = !item.parent ? state.itemTree : state.itemMap[item.parent].children;

      // Take item out from the old parent
      oldParent.splice(oldOrder, 1);
      // Assign it to the new one in order
      newParent.splice(item.order, 0, editedItem);

      // if parent changed rewrite order in the old parent
      if (oldParent !== newParent) oldParent.forEach((elem, index) => { elem.order = index; });
      // then rewrite order in the new parent
      newParent.forEach((elem, index) => { elem.order = index; });

      // Recalc flatten tree
      let newItems = [];
      let stack = [...state.itemTree];
      while (stack.length) {
        const top = stack.pop();
        newItems.push(top);
        stack.concat(top.children);
      }
      state.items = newItems;
      state.isLoaded = false; // Force reload on next view change
    },

    rm: (state, item) => {
      if (!state.itemMap[item.id]) {
        console.warning('No such item ', item.id);
        return;
      }
      // Find the old element
      const oldItem = state.itemMap[item.id];
      const parent = !oldItem.parent ? state.itemTree : state.itemMap[oldItem.parent].children;
      const itemIndex = parent.findIndex((elem) => elem.id === item.id);
      // Take it's children
      const children = oldItem.children;
      // Remove old element from the tree && from map
      parent.splice(itemIndex, 1);
      delete state.itemMap[item.id];
      // Place old elements children them where the old element was
      parent.splice(itemIndex, 0, ...children);
      // recalculate order
      parent.forEach((elem, index) => { elem.order = index; });
      // Recalculate flatten tree
      let newItems = [];
      let stack = [...state.itemTree];
      while (stack.length) {
        const top = stack.pop();
        newItems.push(top);
        stack.concat(top.children);
      }
      state.items = newItems;
      state.isLoaded = false; // Force reload on next view change
    },

    set: (state, { property, value }) => {
      state[property] = value;
    }
  },

  actions: {
    pushLoad: common.actions['pushLoad'],
    popLoad: common.actions['popLoad'],

    async fetchAll ({ commit, dispatch, state }) {
      // Ensure it's loaded only once
      if (state.isLoaded) {
        return;
      }
      dispatch('pushLoad');
      await io.categories
        .fetchAll()
        .then((items) => {
          commit('clear');
          items.forEach((item) => {
            commit('put', item);
          });
          state.isLoaded = true;
        })
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => dispatch('popLoad'));
    },

    addNew ({ commit, dispatch, state }, { parent, name }) {
      name = name && name.trim();
      if (!name) {
        return;
      }
      const newItem = {
        name,
        parent: parent ? parent.id : null,
        order: parent ? parent.children.length : state.itemTree.length
      };
      dispatch('pushLoad');
      return io.categories
        .add(newItem)
        .then((item) => { commit('put', item); })
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => dispatch('popLoad'));
    },

    edit ({ commit, dispatch, state }, item) {
      item.name = item.name.trim();

      if (!item.name) {
        // TODO: Sup bro, you sure?
        dispatch('pushLoad');
        return io.categories.remove(item)
          .then((item) => commit('re#move', item))
          .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
          .finally(() => dispatch('popLoad'));
      } else {
        dispatch('pushLoad');
        return io.categories
          .edit(item)
          .then((edited) => commit('edit', edited))
          .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
          .finally(() => dispatch('popLoad'));
      }
    },

    remove ({ commit, state, dispatch }, item) {
      dispatch('pushLoad');
      return io.categories
        .remove(item)
        .then(() => commit('rm', item))
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => dispatch('popLoad'));
    },

    move ({ commit, dispatch }, { item, index, parentId }) {
      const oldParentId = item.parent;
      const oldOrder = item.order;
      item.parent = parentId;
      item.order = index;
      dispatch('pushLoad');
      return io.categories
        .edit(item)
        .then((edited) => {
          commit('edit', edited);
          commit('reorder', { item: edited, oldParentId, oldOrder });
        })
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => dispatch('popLoad'));
    }

  }
};
