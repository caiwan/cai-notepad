import Vue from 'vue';
import Vuex from 'vuex';

// import createPersistedState from 'vuex-persistedstate';

import Todos from './todosStore';
import Notes from './notesStore';
import UI from './ui'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    Todos, Notes, UI
  },

  plugins: [
    // none
  ]
});
