
export default {
  namespaced: true,
  state: {
    showSidebar: false,
    showSnackbar: false,
    snackbarMessages: []
  },

  getters: {
    isLoading(state, gaetters, rootState, rootGetters) {
      return rootState.App.isInitializing
        || rootState.Notes.isLoading
        || rootState.Tasks.isLoading
        ;
    },
  },

  mutations: {
    toggle: (state, property) => state[property] = !state[property],
    pushSnackbar(state, message) {
      state.snackbarMessages.push(message);
      state.showSnackbar = true;
    },
    pullSnackbar(state) {
      state.snackbarMessages = [];
      state.showSnackbar = false;
    }
  },

  actions: {
    pushIOError({ commit }, error) {
      commit('pushSnackbar', `IO error ${error.status}: ${error.statusText}`);
    }
  }

}
