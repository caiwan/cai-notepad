import io from '@/services/io';
import common, { copyObject } from '@/store/_common';

export default {
  namespaced: true,

  state: {
    items: []
  },

  getters: {
  },

  mutations: {
    ...common.mutations
  },

  actions: {
    fetchSettings () {

    },
    addSetting () {

    },
    editSetting () {

    },
    deleteSetting () {

    }
  }
};
