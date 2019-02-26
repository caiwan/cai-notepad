export default {
  namespaced: true,
  state: {
    isInitializing: true
  },
  mutations: {
    initialized: (state) => {
      state.isInitializing = false;
    }
  }
};
