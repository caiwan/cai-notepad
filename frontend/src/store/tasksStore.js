import io from '@/services/io';
import filters from '@/services/filters';
import common from '@/store/_common';

export default {
  namespaced: true,

  state: {
    items: [],
    visibility: 'all',
    categoryFilter: 'all',
    milestoneFilter: 'all',
    isLoading: false,
    colorMap: []
  },

  getters: {
    filtered: state => filters[state.visibility](state.items),
    remaining: state => filters.active(state.items).length,
    archived: state => state.items.filter(item => item.is_archived),
    colors: () => io.settings['tasks']['priority_colors'] || [],
    colorName: (state) => (name) => state.colorMap[name] || 'none'
  },

  mutations: {
    ...common.mutations,
    show (state, filterName) {
      if (filters.hasOwnProperty(filterName)) { state.visibility = filterName; }
    }
  },

  actions: {
    ...common.actions,
    async fetchAll ({ state, commit, dispatch, getters }) {
      dispatch('pushLoad');
      await io.tasks.fetchAll({
        category: state.categoryFilter,
        milestone: state.milestoneFilter
      })
        .then((items) => {
          commit('clear');
          commit('putAll', items);
          getters.colors.forEach((color) => { state.colorMap[color.value] = color.name; });
          return items;
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });
    },

    updateFilters ({ state, commit }, { categoryId, milestoneId }) {
      commit('set', { property: 'categoryFilter', value: categoryId });
      commit('set', { property: 'milestoneFilter', value: milestoneId });
    },

    async addNew ({ commit, dispatch }, value) {
      value.title = value.title && value.title.trim();
      if (!value.title) {
        return;
      }
      dispatch('pushLoad');
      await io.tasks.add({
        title: value.title,
        is_completed: false,
        category: value.category
      }).then((item) => {
        commit('put', item);
      })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });
    },

    async toggleCompleted ({ commit, dispatch }, item) {
      if (!item) {
        return;
      }
      item.is_completed = !item.is_completed;
      dispatch('pushLoad');
      await io.tasks.edit(item)
        .then((edited) => {
          commit('edit', edited);
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });
    },

    async edit ({ dispatch, commit, state }, item) {
      item.title = item.title.trim();
      // Remove when we've deleted the title and committed
      if (!item.title) {
        dispatch('remove', item); // this will update filters anyway
      } else {
        // Save otherwise
        dispatch('pushLoad');
        await io.tasks.edit(item)
          .then((edited) => {
            commit('edit', edited);
          })
          .catch(error => dispatch('UI/pushIOError', error, { root: true }))
          .finally(() => { dispatch('popLoad'); });
      }
    },

    async remove ({ commit, dispatch }, item) {
      await io.tasks.remove(item)
        .then(() => {
          commit('rm', item);
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });
    },

    async toggleArchive ({ commit, dispatch }, item) {
      item.is_archived = !item.is_archived;
      // completed && archived -> not completed && not archived
      item.is_completed = !item.is_archived ? false : item.is_completed;
      dispatch('pushLoad');
      await io.tasks.edit(item)
        .then((edited) => {
          commit('edit', edited);
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });
    },

    archiveCompleted ({ commit, dispatch, state }) {
      // TODO: Might be a good idea if it would be a server-side task
      state.items.forEach(async element => {
        if (element.is_completed) {
          element.is_archived = true;
          dispatch('pushLoad');
          await io.tasks.edit(element)
            .then((edited) => {
              commit('edit', edited);
            })
            .catch(error => dispatch('UI/pushIOError', error, { root: true }))
            .finally(() => { dispatch('popLoad'); });
        }
      });
    },

    setAllDone ({ commit, dispatch, state }) {
      state.items.forEach(async element => {
        if (!element.is_completed) {
          // TODO: Might be a good idea if it would be a server-side task
          element.is_completed = true;
          dispatch('pushLoad');
          await io.tasks.edit(element)
            .then((edited) => {
              commit('edit', edited);
            })
            .catch(error => dispatch('UI/pushIOError', error, { root: true }))
            .finally(() => { dispatch('popLoad'); });
        }
      });
    }

  }

};
