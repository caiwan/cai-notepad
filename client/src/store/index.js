import Vue from 'vue';
import Vuex from 'vuex';

import Tasks from './tasksStore';
import Notes from './notesStore';
import Categories from './categoryStore';
import UI from './ui';
import App from './app';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    Tasks, Notes, Categories, UI, App
  }
});
