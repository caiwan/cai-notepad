import io from '@/services/io';
import common from '@/store/_common';

export default {
  namespaced: true,

  state: {
    items: [],
    editingItem: null,
    beforeEditCache: "",
  },

  getters: {
    // ... 
  },

  mutations: {
    ...common.mutations,
  },

  actions: {

    async fetchAll({
      commit
    }) {
      const items = await io.categories.fetchAll();
      commit("clear");
      commit("putAll", items);
    },

    async addNew({
      commit,
      state
    }, { parent, value }) {
      console.log('hello', { parent, value });
      value = value && value.trim();
      if (!value) {
        return;
      }
      const item = await io.categories.add({
        title: value,
        parent: parent
      });
      commit("put", item);
    },

    startEdit({
      commit,
      state
    },
      item) {
      state.beforeEditCache = item.title;
      state.editingItem = item;
    },

    async doneEdit({
      commit,
      state
    },
      item) {
      if (!state.editingItem) {
        return;
      }

      if (item.title.trim() == state.beforeEditCache) {
        state.editingItem = null;
        return;
      }

      item.title = item.title.trim();
      if (!item.title) {
        await io.todos.remove(item);
        commit("remove", item);
      } else {
        const edited = await io.todos.edit(item);
        commit("edit", edited);
      }
      state.editingItem = null;
    },

    cancelEdit({
      commit,
      state
    },
      item) {
      item.title = this.beforeEditCache;
      state.editingItem = null;
      this.beforeEditCache = "";
    },

    async remove({
      commit
    }, item) {
      await io.categories.remove(item);
      commit("rm", item);
    },

  }

}
