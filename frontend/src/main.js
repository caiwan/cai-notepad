import 'node-snackbar';

import Vue from 'vue';
import App from './App';
import { router } from './router';
import store from './store';

import io from './services/io';

import VueMarkdown from 'vue-markdown';

import GAuth from 'vue-google-oauth2';

io.initialized.then(settings => {
  if (!settings.hasOwnProperty('oauth-google') || !settings['oauth-google']['enabled']) {
    console.info('Google authentication was not set up or is not enabled');
    return settings;
  }
  const gauthOption = {
    clientId: settings['oauth-google']['client_id'],
    scope: settings['oauth-google']['scope'],
    prompt: 'select_account'
  };
  Vue.use(GAuth, gauthOption);
  console.log('gauthOption', { gauthOption });
  return settings;
});

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
