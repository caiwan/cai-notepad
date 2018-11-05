import io from '@/services/io';
import common from '@/store/_common';

import tags from './notes/tagsStore'

export default {
  namespaced: true,

  modules: {
    "Tags": tags
  },

  state: {
    items: [],
    editingItem: null,
    beforeEditCache: null,
    isDirty: false // TODO: ... 
  },

  mutations: {
    ...common.mutations,
    show(state, filterName) {
      if (filters[filterName]) {
        state.visibility = filterName;
      }
    },
  },

  actions: {
    async fetchAll({
      commit
    }) {
      const items = await io.notes.fetchAll();
      commit("clear");
      commit("putAll", items);
    },

    async addNew({
      commit
    }, value) {
      value.title = value.title && value.title.trim();
      value.content = value.content && value.content.trim();
      if (!value.title && !value.content) {
        return;
      }
      const item = await io.notes.add({
        ...value
      });

      commit("putFront", item);
    },

    async togglePin({
      commit
    }, item) {
      console.error('Not implemented');
    },

    startEdit({
      state
    },
      item) {
      state.beforeEditCache = {
        title: item.title,
        content: item.content,
      };
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

      // TODO: save only when document is dirty -> component

      item.title = item.title.trim();
      if (!item.title) {
        await io.notes.remove(item);
        commit("remove", item);
      } else {
        const edited = await io.notes.edit(item);
        commit("edit", edited);
      }

      state.editingItem = null;
    },

    cancelEdit({
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
      await io.notes.remove(item);
      commit("rm", item);
    },

    async archive({
      commit
    }, item) {
      console.error('Not implemented');
    },
  }

}
