import 'node-snackbar';

import Vue from 'vue';
import App from './App';
import { router } from './router';
import store from './store';

import VueMarkdown from 'vue-markdown';

Vue.config.productionTip = false;
Vue.component('vue-markdown', VueMarkdown);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {
    App
  },
  template: '<App/>'
});
