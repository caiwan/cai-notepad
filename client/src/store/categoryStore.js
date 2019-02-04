import io from '@/services/io';

export default {
  namespaced: true,

  state: {
    items: [],
    itemMap: [],
    itemTree: []
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

    async fetchAll ({ commit, dispatch }) {
      const items = await io.categories.fetchAll().catch(error => dispatch('UI/pushIOError', error, { root: true }));
      if (items) {
        commit('clear');
        items.forEach(item => {
          commit('put', item);
        });
      }
    },

    async addNew ({ commit, state, dispatch }, { parent, value }) {
      console.log('Lol', value);
      value = value && value.trim();

      if (!value) {
        return;
      }

      const item = await io.categories.add({
        title: value,
        parent: parent
      }).catch(error => dispatch('UI/pushIOError', error, { root: true }));
      if (!item) { return; }

      commit('put', item);
    },

    async edit ({ commit, dispatch }, item) {
      // console.log('Edit', item);
      item.title = item.title.trim();
      if (!item.title) {
        await io.categories.remove(item);
        commit('remove', item);
      } else {
        const edited = await io.categories.edit(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
        if (!edited) { return; }
        commit('edit', edited);
      }
    },

    async remove ({ commit, dispatch }, item) {
      await io.categories.remove(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
      commit('rm', item);
    }

  }

};
