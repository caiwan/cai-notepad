import io from '@/services/io';
import common from '@/store/_common';

const TAGS_MAX = 10;

export default {
  namespaced: true,

  state: {
    items: [],
    isLoading: false
  },

  mutations: {
    ...common.mutations
  },

  actions: {
    async queryAutocomplete ({ state, commit }, query) {
      if (query.length < 3) { return; }
      // This loading sequence will handled separately, inside the component
      state.isLoading = true;
      await io.tags.queryAutocomplete(query, TAGS_MAX)
        .then((items) => {
          commit('clear');
          commit('putAll', items);
        })
        .finally(() => { state.isLoading = false; });
    }
  }

};
