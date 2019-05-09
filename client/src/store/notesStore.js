import io from '@/services/io';
import common from '@/store/_common';
import tags from './notes/tagsStore';

export default {
  namespaced: true,

  modules: {
    'Tags': tags
  },

  state: {
    items: [],
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
    ...common.actions,
    fetchAll ({ commit, dispatch, state }) {
      dispatch('pushLoad');
      return io.notes.fetchAll({
        category: state.categoryFilter,
        milestone: state.milestoneFilter
      })
        .then((items) => {
          commit('clear');
          commit('putAll', items);
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => {
          dispatch('popLoad');
        });
    },

    updateFilters ({ commit, state }, { categoryId, milestoneId }) {
      commit('set', { property: 'categoryFilter', value: categoryId });
      commit('set', { property: 'milestoneFilter', value: milestoneId });
    },

    async addNew ({ commit, dispatch }, newItem) {
      newItem.title = newItem.title && newItem.title.trim();
      newItem.content = newItem.content && newItem.content.trim();
      if (!newItem.title && !newItem.content) {
        return;
      }
      dispatch('pushLoad');
      await io.notes.add({
        ...newItem
      })
        .then((item) => { commit('putFront', item); })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => {
          dispatch('popLoad');
        });
    },

    async edit ({ commit, dispatch, state }, editedItem) {
      editedItem.title = editedItem.title.trim();
      dispatch('pushLoad');
      await io.notes.edit(editedItem)
        .then((item) => {
          commit('edit', item);
          commit('bump', editedItem);
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => dispatch('popLoad'));
    },

    async remove ({ dispatch, commit }, item) {
      dispatch('pushLoad');
      await io.notes.remove(item)
        .then((item) => {
          commit('rm', item);
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => dispatch('popLoad'));
    },

    async togglePin ({ commit, dispatch, state }, item) {
      item.is_pinned = !item.is_pinned;
      if (state.editingItem !== item) {
        dispatch('pushLoad');
        await io.notes.edit(item)
          .then((item) => {
            commit('edit', item);
          })
          .catch(error => dispatch('UI/pushIOError', error, { root: true }))
          .finally(() => dispatch('popLoad'));
      }
    },

    async toggleArchive ({ commit, dispatch, state }, item) {
      item.is_archived = !item.is_archived;
      if (state.editingItem !== item) {
        dispatch('pushLoad');
        await io.notes.edit(item)
          .then((item) => {
            commit('edit', item);
          })
          .catch(error => dispatch('UI/pushIOError', error, { root: true }))
          .finally(() => dispatch('popLoad'));
      }
    }
  }

};
