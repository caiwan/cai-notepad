import Vue from 'vue';
import Vuex from 'vuex';

// import createPersistedState from 'vuex-persistedstate';

import Todos from './todos';
import Notes from './notes';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    Todos, Notes
  },

  plugins: [
    // none
  ]
});
