
export default {
  namespaced: true,
  state: {
    showSidebar: false,
    showSnackbar: false,
    showUserMenu: false,
    snackbarMessages: [],
    snackbarTimeout: null,
    loading: 0
  },

  getters: {
    isLoading (state, getters, rootState) { return !!state.loading || rootState.App.isInitializing; }
  },

  mutations: {
    toggle: (state, property) => { state[property] = !state[property]; },
    pushSnackbar (state, message) {
      state.snackbarMessages.push(message);
      state.showSnackbar = true;
    },
    pullSnackbar (state) {
      state.snackbarMessages = [];
      state.showSnackbar = false;
      state.snackbarTimeout = null;
    }
  },

  actions: {
    pushIOError ({ state, commit }, error) {
      console.error('snackbar', error);
      commit('pushSnackbar', `${error}`);
      if (state.snackbarTimeout) clearTimeout(state.snackbarTimeout);
      state.snackbarTimeout = setTimeout(() => { commit('pullSnackbar'); }, 3000);
    },
    pushLoad ({ state }) { ++state.loading; },
    popLoad ({ state }) { --state.loading; if (state.loading < 0) { console.error('loading queue underflows'); state.loading = 0; } }
  }

};
