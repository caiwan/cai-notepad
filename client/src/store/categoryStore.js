import io from '@/services/io';
import common from '@/store/_common';

export default {
  namespaced: true,

  state: {
    items: [],
    itemMap: [],
    itemTree: [],
    isLoading: false,
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

    reorder: (state, item) => {
      // find the parent where the item was
      const oldItem = state.itemMap[item.id];
      const oldParent = !oldItem.parent ? state.itemTree : state.itemMap[oldItem.parent].children;
      // find the parent where the item is supposed to be
      const newParent = !item.patent ? state.itemTree : state.itemMap[item.parent].children;
      // rewrite order in the new parent
      newParent.forEach((elem, index) => { elem.order = index; });
      // if parent changed rewrite order in the old parent
      if (oldItem.parent !== item.parent) oldParent.forEach((elem, index) => { elem.order = index; });

      // Recalc spantree
      let newItems = [];
      let stack = [...state.itemTree];
      while (stack.length) {
        const top = stack.pop();
        newItems.push(top);
        stack.concat(newItems.children);
      }
      state.items = newItems;
    },

    rm: (state, item) => {
      state.items.splice(state.items.indexOf(item), 1);
      state.itemMap.splice(state.items.indexOf(item), 1);
      state.itemTree.splice(state.itemTree.indexOf(item), 1); // ? is it works for real?
    },

    set: (state, { property, value }) => {
      state[property] = value;
    },
    fetchStart: common.mutations['fetchStart'],
    fetchEnd: common.mutations['fetchEnd']
  },

  actions: {
    async fetchAll ({ commit, dispatch, state }) {
      // Ensure it's loaded only once
      if (state.isLoaded) {
        return;
      }
      commit('fetchStart');
      await io.categories
        .fetchAll()
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .then((items) => {
          commit('clear');
          items.forEach((item) => {
            commit('put', item);
          });
          state.isLoaded = true;
        });
      commit('fetchEnd');
    },

    addNew ({ commit, dispatch, state }, { parent, name }) {
      name = name && name.trim();
      if (!name) {
        return;
      }

      state.isLoading = true;

      const newItem = {
        name,
        parent: parent ? parent.id : null,
        order: parent ? parent.children.length : state.itemTree.length
      };

      return io.categories
        .add(newItem)
        .then((item) => { commit('put', item); })
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { state.isLoading = false; });
    },

    edit ({ commit, dispatch, state }, item) {
      item.name = item.name.trim();
      state.isLoading = true;

      if (!item.name) {
        // TODO: Sup bro, you sure?
        return io.categories.remove(item)
          .then((item) => commit('re#move', item))
          .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
          .finally(() => { state.isLoading = false; });
      } else {
        return io.categories
          .edit(item)
          .then((edited) => commit('edit', edited))
          .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
          .finally(() => { state.isLoading = false; });
      }
    },

    remove ({ commit, state, dispatch }, item) {
      state.isLoading = true;
      return io.categories
        .remove(item)
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .then((item) => commit('rm', item))
        .finally(() => { state.isLoading = false; });
    },

    move ({ commit, state, dispatch }, { item, newIndex, newParentId }) {
      // item.newParentId =
      return io.categories
        .edit(item)
        .then((edited) => {
          commit('edit', edited);
          commit('reorder', edited);
        })
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { state.isLoading = false; });
    }

  }
};
