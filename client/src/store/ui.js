
export default {
  namespaced: true,
  state: {
    showSidebar: false,
    showSnackbar: false,
    showUserMenu: false,
    snackbarMessages: [],
    loading: 0
  },

  getters: {
    isLoading (state, getters, rootState) { return !!state.loading || rootState.App.isInitializing; }
  },

  mutations: {
    toggle: (state, property) => { state[property] = !state[property]; },
    pushSnackbar ({ dispatch, state }, message) {
      state.snackbarMessages.push(message);
      state.showSnackbar = true;
      setTimeout(() => { dispatch('pullSnackbar'); }, 3000);
    },
    pullSnackbar (state) {
      state.snackbarMessages = [];
      state.showSnackbar = false;
    }
  },

  actions: {
    pushIOError ({ commit }, error) {
      console.error(error);
      commit('pushSnackbar', `${error}`);
    },
    pushLoad ({ state }) { ++state.loading; },
    popLoad ({ state }) { --state.loading; if (state.loading < 0) { console.error('loading queue underflows'); state.loading = 0; } }
  }

};
