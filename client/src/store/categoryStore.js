import io from '@/services/io';
import common from '@/store/_common';

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
    category: (state) => (id) => id in state.itemMap ? state.itemMap[id] : null,
    categoryName: (state) => (id) => id in state.itemMap ? state.itemMap[id].name : 'Unassigned'
  },

  mutations: {
    clear: (state) => { state.items = []; state.itemMap = []; state.itemTree = []; },
    put: (state, item) => {
      if (!item.hasOwnProperty('children')) { item['children'] = []; }
      state.itemMap[item.id] = item;
      if (item.parent) {
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

    rm: (state, item) => {
      state.items.splice(state.items.indexOf(item), 1);
      state.itemMap.splice(state.items.indexOf(item), 1);
      state.itemTree.splice(state.itemTree.indexOf(item), 1); // ? is it works for real?
    },

    set: (state, { property, value }) => { state[property] = value; },
    fetchStart: common.mutations['fetchStart'],
    fetchEnd: common.mutations['fetchEnd']

  },

  actions: {

    async fetchAll ({ commit, dispatch, state }) {
      // Ensure it's loaded only once
      if (state.isLoaded) { return; }
      commit('fetchStart');
      await io.categories.fetchAll().catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .then((items) => {
          commit('clear');
          console.log('Fetch Items', items);
          items.forEach(item => {
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

      await io.categories.add({
        name, parent: parent ? parent.id : null
      })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .then((item) => commit('put', item));

      state.isLoading = false;
    },

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
        await io.categories.edit(item)
          .catch(error => dispatch('UI/pushIOError', error, { root: true }))
          .then((edited) => commit('edit', edited));
      }
      state.isLoading = false;
    },

    async remove ({ commit, state, dispatch }, item) {
      state.isLoading = true;
      await io.categories.remove(item)
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .then((item) => commit('rm', item));
      state.isLoading = false;
    },

    async move ({ commit, state, dispatch }, { item, newParent }) {
      item.parent = newParent ? newParent.id : null;
      await io.categories.edit(item).catch(error => dispatch('UI/pushIOError', error, { root: true }))
        // TODO: re-order items ?
        // TODO modify items[] and itemTree[] ?
        .then((edited) => { commit('edit', edited); });
    },

    async mergeUp ({ commit, state, dispatch }, { item }) {
      // TODO: ...
    }
  }

};
