import io from '@/services/io';

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
    getCategory: (state) => (id) => id in state.items ? state.items[id] : null
  },

  mutations: {
    clear: (state) => { state.items = []; state.itemMap = []; state.itemTree = []; },
    put: (state, item) => {
      if (!item.hasOwnProperty('children')) { item['children'] = []; }
      state.itemMap[item.id] = item;
      if (item.parent) {
        const pid = item.parent.id;
        state.itemMap[pid].children.push(state.itemMap[item.id]);
      } else {
        state.itemTree.push(state.itemMap[item.id]);
      }
      state.items.push(item);
    },

    edit: (state, item) => {
      var storedItem = state.itemMap[item.id];
      for (var key in item) {
        if (item.hasOwnProperty(key)) {
          storedItem[key] = item[key];
        }
      }
    },

    rm: (state, item) => {
      state.items.splice(state.items.indexOf(item), 1);
      state.itemMap.splice(state.items.indexOf(item), 1);
      state.itemTree.splice(state.itemTree.indexOf(item), 1); // ? is it worksfor real?
    }

  },

  actions: {

    async fetchAll ({ commit, dispatch, state }) {
      // Ensure it's loaded only once
      if (state.isLoaded) { return; }
      state.isLoading = true;
      const items = await io.categories.fetchAll().catch(error => dispatch('UI/pushIOError', error, { root: true }));
      if (items) {
        commit('clear');
        items.forEach(item => {
          commit('put', item);
        });
        state.isLoaded = true;
      }
      state.isLoading = false;
    },

    async addNew ({ commit, dispatch, state }, { parent, name }) {
      name = name && name.trim();
      console.log('Lol', { parent, name });
      if (!name) {
        return;
      }

      state.isLoading = true;

      const item = await io.categories.add({
        name, parent
      }).catch(error => dispatch('UI/pushIOError', error, { root: true }));
      if (!item) { return; }

      commit('put', item);

      state.isLoading = false;
    },

    async edit ({ commit, dispatch, state }, item) {
      item.name = item.name.trim();
      state.isLoading = true;

      if (!item.name) {
        await io.categories.remove(item);
        commit('remove', item);
      } else {
        // TODO: Sup bro, you sure?
        const edited = await io.categories.edit(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
        if (!edited) { return; }
        commit('edit', edited);
      }
      state.isLoading = false;
    },

    async remove ({ commit, state, dispatch }, item) {
      state.isLoading = true;
      await io.categories.remove(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
      commit('rm', item);
      state.isLoading = false;
    }

  }

};
