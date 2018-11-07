
export default {
  namespaced: true,
  state: {
    showSidebar: false
  },
  getters: {
    isLoading() {
      return false;
    }
  },
  mutations: {
    toggle: (state, property) => state[property] = !state[property]
  }
}
