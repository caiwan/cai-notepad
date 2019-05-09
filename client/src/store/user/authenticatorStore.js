import io from '@/services/io';
import common from '@/store/_common';

export default {
  namespaced: true,

  state: {
    items: [],
    isLoading: false
  },

  getters: {
    isAuthenticated: (state) => (idpId) => !!state.items[idpId],
    getAuthenticators: (state) => (idpId) => state.items[idpId] || null
  },

  mutations: {
    clear: (state) => { state.items = []; },
    put: (state, item) => {
      if (!state.items.hasOwnProperty(item['idp_id'])) { state.items[item['idp_id']] = []; }
      state.items[item.idp_id].push(item);
    }
  },

  actions: {
    pushLoad: common.actions['pushLoad'],
    popLoad: common.actions['popLoad'],

    async fetchAll ({ commit, dispatch, state }) {
      dispatch('pushLoad');
      await io.authenticators.fetchAll()
        .then((items) => {
          commit('clear');
          items.forEach((item) => commit('put', item));
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });
    },

    async signIn ({ dispatch, state }, { service, tokens }) {
      dispatch('pushLoad');
      await io.authenticators.add(service, tokens)
        .then(dispatch('fetchAll'))
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });

      state.isLoading = false;
    },

    async signOut ({ dispatch, state }, item) {
      dispatch('pushLoad');
      await io.authenticators.remove(item.id)
        .then(dispatch('fetchAll'))
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });
    }

  }
};
