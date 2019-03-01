import io from '@/services/io';
import common, { copyObject } from '@/store/_common';

export default {
  namespaced: true,

  state: {
    items: [],
    isLoading: false

  },

  getters: {

  },

  mutations: {
    ...common.mutations
  },

  actions: {
    async fetchAll ({ commit, dispatch }) {
      commit('fetchStart');
      await io.authenticators.fetchAll()
        .then((items) => {
          commit('clear');
          commit('putAll', items);
        })
        .catch(error => dispatch('UI/pushIOError', error, { root: true }));
      commit('fetchEnd');
    },

    async signIn ({ dispatch, commit }, { service, authCode }) {
      await io.authenticators.add(service, authCode)
        .then(dispatch('fetchAll'))
        .catch(error => dispatch('UI/pushIOError', error, { root: true }));
    },

    async signOut ({ dispatch, commit }, { service }) {
      // await ...
      console.log('kkthxbai', { service });
    }

  }
};
