import userSettings from './user/settingStore';
import authenticators from './user/authenticatorStore';
import syncGoogle from './user/syncGoogleStore';
import io from '../services/io';
import { router } from '../router';

import common from '@/store/_common';

let user = null;
try {
  user = JSON.parse(localStorage.getItem('user'));
} catch (e) {
  localStorage.removeItem('user');
  user = null;
}

export default {
  namespaced: true,

  modules: {
    'SyncGoogle': syncGoogle,
    'Settings': userSettings,
    'Authenticators': authenticators
  },

  state: {
    status: { loggedIn: !!user },
    user
  },

  getters:
  {
    isLoggedIn: (state) => state.status && state.status.loggedIn
  },

  mutations:
  {
    loginSuccess (state, user) {
      state.status = { loggedIn: true };
      state.user = user;
    },
    logout (state) {
      state.status = { loggedIn: false };
      state.user = null;
    }
  },

  actions: {
    pushLoad: common.actions['pushLoad'],
    popLoad: common.actions['popLoad'],

    async fetchProfile ({ dispatch, commit, getters, state }) {
      if (!getters.isLoggedIn) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        return;
      }
      dispatch('pushLoad');
      await io.user.fetchProfile()
        .then(user => {
          localStorage.setItem('user', JSON.stringify(user));
          commit('loginSuccess', user);
        })
        .catch(error => {
          dispatch('UI/pushIOError', error, { root: true });
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          commit('logout');
          router.push('/login');
        })
        .finally(() => { dispatch('popLoad'); });
    },

    login ({ dispatch, commit }, { username, password }) {
      if (!username || !password) { return; }
      dispatch('pushLoad');
      return io.user.login(username, password)
        .then(response => { localStorage.setItem('token', response.token); })
        .then(() => { io.updateHeader(); })
        .then(() => { return io.user.fetchProfile(); })
        .then(user => {
          localStorage.setItem('user', JSON.stringify(user));
          commit('loginSuccess', user);
        })
        .then(() => { router.push('/'); })
        .catch(error => {
          dispatch('UI/pushIOError', error, { root: true });
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          commit('logout');
          router.push('/login');
        })
        .finally(() => { dispatch('popLoad'); });
    },

    logout ({ dispatch, commit }) {
      dispatch('pushLoad');
      return io.user.logout()
        .then(() => {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        })
        .then(() => { commit('logout'); })
        .then(() => { router.push('/login'); })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .finally(() => { dispatch('popLoad'); });
    },

    register ({ dispatch, commit }, user) {
      alert('OvO');
    }
  }
};
