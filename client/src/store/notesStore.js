import io from '@/services/io';
import filters from '@/services/filters';
import common from '@/store/_common';
import tags from './notes/tagsStore';

export default {
  namespaced: true,

  modules: {
    'Tags': tags
  },

  state: {
    items: [],
    editingItem: null,
    beforeEditCache: null,
    isDirty: false,
    filteredItems: [],
    categoryFilter: 'all',
    milestoneFilter: 'all',
    isLoading: false
  },

  getters: {
    pinnedItems: state => state.filteredItems.filter(item => item.is_archived === false && item.is_pinned === true),
    defaultItems: state => state.filteredItems.filter(item => item.is_archived === false && item.is_pinned === false),
    archivedItems: state => state.filteredItems.filter(item => item.is_archived === true)
  },

  mutations: {
    ...common.mutations,
    bump: (state, item) => state.items.sort((a, b) => a === item ? -1 : b === item ? 1 : 0),
    updateFilteredItems (state) {
      state.filteredItems = filters.all(
        state.items, state.milestoneFilter, state.categoryFilter
      );
    }
  },

  actions: {
    async fetchAll ({ commit, dispatch }) {
      commit('fetchStart');
      const items = await io.notes.fetchAll().catch(error => dispatch('UI/pushIOError', error, { root: true }));
      if (items) {
        commit('clear');
        commit('putAll', items);
      }
      commit('fetchEnd');
    },

    updateFilters ({ commit, state }, { categoryId, milestoneId }) {
      commit('set', { property: 'categoryFilter', value: categoryId });
      commit('set', { property: 'milestoneFilter', value: milestoneId });
      commit('updateFilteredItems');
    },

    async addNew ({ commit, dispatch }, value) {
      value.title = value.title && value.title.trim();
      value.content = value.content && value.content.trim();
      if (!value.title && !value.content) {
        return;
      }
      const item = await io.notes.add({
        ...value
      }).catch(error => dispatch('UI/pushIOError', error, { root: true }));
      if (!item) return;

      commit('putFront', item);
      commit('updateFilteredItems');
    },

    startEdit ({ dispatch, state }, item) {
      state.beforeEditCache = Object.assign(item, {});
      state.editingItem = item;
    },

    async doneEdit ({ commit, dispatch, state }, item) {
      if (!state.editingItem) {
        return;
      }
      item.title = item.title.trim();
      const edited = await io.notes.edit(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
      if (!edited) return;
      commit('edit', edited);

      state.editingItem = null;

      // bring my post up
      commit('bump', item);
      commit('updateFilteredItems');
    },

    cancelEdit ({ dispatch, state }, item) {
      item = Object.assign(state.beforeEditCache, item);
      state.editingItem = null;
      this.beforeEditCache = null;
    },

    async remove ({ dispatch, commit }, item) {
      await io.notes.remove(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
      commit('rm', item);
      commit('updateFilteredItems');
    },

    async togglePin ({ commit, dispatch, state }, item) {
      item.is_pinned = !item.is_pinned;
      if (state.editingItem !== item) {
        const edited = await io.notes.edit(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
        if (!edited) return;
        commit('edit', edited);
      }
    },

    async toggleArchive ({ commit, dispatch, state }, item) {
      item.is_archived = !item.is_archived;
      if (state.editingItem !== item) {
        const edited = await io.notes.edit(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
        if (!edited) return;
        commit('edit', edited);
      }
    }
  }

};
