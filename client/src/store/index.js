import Vue from 'vue';
import Vuex from 'vuex';

// import createPersistedState from 'vuex-persistedstate';

import Todos from './todosStore';
import Notes from './notesStore';
import Categories from './categoryStore';
import UI from './ui'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    Todos, Notes, Categories, UI
  },

  plugins: [
    // none
  ]
});
