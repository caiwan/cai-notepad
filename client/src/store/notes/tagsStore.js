import io from '@/services/io';
import common from '@/store/_common';

const TAGS_MAX = 10;

export default {
  namespaced: true,

  state: {
    items: [],
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
    async queryAutocomplete({
      commit
    }, query) {
      if (query.length < 3)
        return;
      const items = await io.tags.queryAutocomplete(query, TAGS_MAX);
      if (items) {
        commit("clear");
        commit("putAll", items);
      }
    }
  }

}
