import io from '@/services/io';

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
    async fetchAll ({ commit, dispatch, state }) {
      state.isLoading = true;
      await io.authenticators.fetchAll()
        .then((items) => {
          commit('clear');
          items.forEach((item) => commit('put', item));
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }));
      state.isLoading = false;
    },

    async signIn ({ dispatch, state }, { service, tokens }) {
      state.isLoading = true;

      await io.authenticators.add(service, tokens)
        .then(dispatch('fetchAll'))
        .catch(error => dispatch('UI/pushIOError', error, { root: true }));
      state.isLoading = false;
    },

    async signOut ({ dispatch, state }, item) {
      state.isLoading = false;
      await io.authenticators.remove(item.id)
        .then(dispatch('fetchAll'))
        .catch(error => dispatch('UI/pushIOError', error, { root: true }));
      state.isLoading = false;
    }

  }
};
