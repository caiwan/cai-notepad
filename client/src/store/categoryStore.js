import io from '@/services/io';
import common, { arrayMove } from '@/store/_common';

function reorder (parent) {
  var count = 0;
  parent.forEach((element) => {
    element.order = 2 * count;
    count++;
  });
}

export default {
  namespaced: true,

  state: {
    items: [],
    itemMap: [],
    itemTree: [],
    isLoading: false,
    isLoaded: false,
    beforeEditCache: {},
    editingItem: null
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
    },
    put: (state, item) => {
      if (!item.hasOwnProperty('children')) {
        item['children'] = [];
      }
      state.itemMap[item.id] = item;
      if (item.parent) {
        if (!state.itemMap[item.parent]) { state.itemMap[item.parent] = { children: [] }; }; // :(
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

    reorder: (state, { edited, oldParent, newParent, newOrder }) => {
      const item = state.itemMap[edited.id]; // Molest the stuff that was already stored
      const oldChildren = oldParent ? oldParent.children : state.itemTree;
      const newChildren = newParent ? newParent.children : state.itemTree;
      const oldId = oldChildren.findIndex((elem) => elem.id === item.id);
      // 1. Has the parent been moved?
      if (oldChildren !== newChildren) {
        oldChildren.splice(oldId, 1);
        // Ordering starts at -1, the element of the one before ea. node, serves a placeholder
        // and incremented by 2
        newChildren.splice(newOrder / 2, 0, item);
      } else {
        // 2. Has the order been moved?
        arrayMove(oldChildren, oldId, newOrder / 2);
      }

      // When item has children, but

      // itemId = state.

      // Recalc older on client side
      // if (oldParent !== newParent) {
      //   let count = 0;
      //   [
      //     oldParent || state.itemTree,
      //     newParent || state.itemTree
      //   ].forEach(parent => parent.forEach(element => {
      //     element.order = 2 * count;
      //     count++;
      //   }));
      // } else {
      //   let count = 0;
      //   (item.parent ? item.parent.children : state.itemTree).forEach(element => {});
      // }
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

    async addNew ({ commit, dispatch, state }, { parent, name }) {
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

      await io.categories
        .add(newItem)
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .then((item) => commit('put', item));

      state.isLoading = false;
    },

    // TODO: Move start, done and cancel editing item to .vue component

    startEdit ({ state }, item) {
      Object.assign(state.beforeEditCache, item);
      state.editingItem = item;
    },

    async doneEdit ({ state, dispatch }, item) {
      await dispatch('edit', item);
      state.beforeEditCache = {};
      state.editingItem = null;
    },

    cancelEdit ({ state, commit }, item) {
      Object.assign(item, state.beforeEditCache);
      state.beforeEditCache = {};
      state.editingItem = null;
    },

    async edit ({ commit, dispatch, state }, item) {
      item.name = item.name.trim();
      state.isLoading = true;

      if (!item.name) {
        // TODO: Sup bro, you sure?
        await io.categories.remove(item);
        commit('remove', item);
      } else {
        await io.categories
          .edit(item)
          .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
          .then((edited) => commit('edit', edited));
      }
      state.isLoading = false;
    },

    async remove ({ commit, state, dispatch }, item) {
      state.isLoading = true;
      await io.categories
        .remove(item)
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .then((item) => commit('rm', item));
      state.isLoading = false;
    },

    async move ({ commit, state, dispatch }, { item, newParent, newOrder }) {
      let oldParent = item.parent ? state.itemMap[item.parent] : null;
      // let oldOrder = item.order;
      item.parent = newParent ? newParent.id : null;

      if (oldParent === newParent || newParent === item || item.order === newOrder) {
        console.log('You simply can\'t.');
        return;
      }

      await io.categories
        .edit(item)
        .catch((error) => dispatch('UI/pushIOError', error, { root: true }))
        .then((edited) => {
          commit('reorder', { edited, oldParent, newParent, newOrder: 0 });
          commit('edit', edited);
        });
    },

    async mergeUp ({ commit, state, dispatch }, { item }) {
      // TODO: ...
    }
  }
};
