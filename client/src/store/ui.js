
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
    // TODO: We will have a loading-stack which operates on a push-pop manner instead
    isLoading (state, getters, rootState) {
      return !!state.loading ||
        rootState.App.isInitializing
      //   // TODO: + User Profile + Settings
      //   rootState.User.isLoading || rootState.User.Authenticators.isLoading ||
      //   rootState.Categories.isLoading ||
      //   rootState.Notes.isLoading ||
      //   rootState.Tasks.isLoading
      ;
    }
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
    }
  },

  actions: {
    pushIOError ({ commit }, error) {
      console.error(error);
      commit('pushSnackbar', `${error}`);
    },
    pushLoad (state) { state.loading++; },
    popLoad (state) { state.loading--; }

  }

};
