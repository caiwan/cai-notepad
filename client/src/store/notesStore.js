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
    categoryFilter: 'all',
    milestoneFilter: 'all',
    isLoading: false
  },

  getters: {
    pinnedItems: state => state.items.filter(item => item.is_archived === false && item.is_pinned === true),
    defaultItems: state => state.items.filter(item => item.is_archived === false && item.is_pinned === false),
    archivedItems: state => state.items.filter(item => item.is_archived === true)
  },

  mutations: {
    ...common.mutations,
    bump: (state, item) => state.items.sort((a, b) => a === item ? -1 : b === item ? 1 : 0)
  },

  actions: {
    async fetchAll ({ commit, dispatch, state }) {
      commit('fetchStart');
      await io.notes.fetchAll({
        category: state.categoryFilter,
        milestone: state.milestoneFilter
      })
        .then((items) => {
          commit('clear');
          commit('putAll', items);
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => {
          commit('fetchEnd'); // TODO: rm this later
        });
    },

    updateFilters ({ commit, state }, { categoryId, milestoneId }) {
      commit('set', { property: 'categoryFilter', value: categoryId });
      commit('set', { property: 'milestoneFilter', value: milestoneId });
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
    },

    cancelEdit ({ dispatch, state }, item) {
      item = Object.assign(state.beforeEditCache, item);
      state.editingItem = null;
      this.beforeEditCache = null;
    },

    async remove ({ dispatch, commit }, item) {
      await io.notes.remove(item).catch(error => dispatch('UI/pushIOError', error, { root: true }));
      commit('rm', item);
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
