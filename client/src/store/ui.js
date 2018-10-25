
export default {
  namespaced: true,
  state: {
    showSidebar: false
  },
  mutations: {
    toggle: (state, property) => state[property] = !state[property]
  }
}
