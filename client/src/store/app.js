export default {
  namespaced: true,
  state: {
    isInitializing: true
  },
  mutations: {
    initialized: (state, initializing) => { state.isInitializing = !initializing; }
  },
  actions: {
    initialized: ({ commit }) => commit('initialized', true)
  }
};
