import userSettings from './user/settingStore';
import authenticators from './user/authenticatorStore';
import syncGoogle from './user/syncGoogleStore';
import io from '../services/io';
import { router } from '../router';

var user = null;
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
    isLoggedIn (state) {
      return state.status && state.status.loggedIn;
    }
  },

  mutations:
  {
    // loginRequest (state, user) {
    // state.status = { loggingIn: true };
    // state.user = user;
    // },
    loginSuccess (state, user) {
      state.status = { loggedIn: true };
      state.user = user;
    },
    // loginFailure (state) {
    // state.status = {};
    // state.user = null;
    // },
    logout (state) {
      state.status = { loggedIn: false };
      state.user = null;
    }
    // registerRequest (state, user) {
    //   state.status = { registering: true };
    // },
    // registerSuccess (state, user) {
    //   state.status = {};
    // },
    // registerFailure (state, error) {
    //   state.status = {};
    // }
  },

  actions: {

    async fetchProfile ({ dispatch, commit }) {
      const user = await io.user.fetchProfile()
        .catch(error => {
          dispatch('UI/pushIOError', error, { root: true });
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          commit('logout');
          router.push('/login');
        });
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
        commit('loginSuccess', user);
      }
    },

    login ({ dispatch, commit }, { username, password }) {
      if (!username || !password) { return; }
      // commit('loginRequest', { username });

      io.user.login(username, password)
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
        });
    },

    logout ({ dispatch, commit, getters }) {
      io.user.logout().catch(error => dispatch('UI/pushIOError', error, { root: true }))
        .then(() => {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        })
        .then(() => { commit('logout'); })
        .then(() => { router.push('/login'); });
    },

    register ({ dispatch, commit }, user) {
      // commit('registerRequest', user);

      // io.user.register(user)
      //   .then(
      //     user => {
      //       commit('registerSuccess', user);
      //       router.push('/login');
      //       setTimeout(() => {
      //         // display success message after route change completes
      //         dispatch('alert/success', 'Registration successful', { root: true });
      //       });
      //     },
      //     error => {
      //       commit('registerFailure', error);
      //       dispatch('alert/error', error, { root: true });
      //     }
      //   );
      console.error('OvO');
    }
  }
};
