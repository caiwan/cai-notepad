import io from '@/services/io';
import common from '@/store/_common';

var filters = {
  all: function (items) {
    return items;
  },
  active: function (items) {
    return items.filter(function (item) {
      return !item.completed;
    });
  },
  completed: function (items) {
    return items.filter(function (item) {
      return item.completed;
    });
  }
};

export default {
  namespaced: true,

  state: {
    items: [],
    editingItem: null,
    beforeEditCache: "",
    visibility: "all"
  },

  getters: {
    filtered: state => {
      return filters[state.visibility](state.items);
    },
    remaining: state => {
      return filters.active(state.items).length;
    },
  },

  mutations: {
    ...common.mutations,

    show(state, filterName) {
      if (filters[filterName]) {
        state.visibility = filterName;
      }
    }
  },

  actions: {

    async fetchAll({
      commit
    }) {
      const items = await io.todos.fetchAll();
      commit("clear");
      commit("putAll", items);
    },

    async addNew({
      commit,
      state
    }, value) {
      value = value && value.trim();
      if (!value) {
        return;
      }
      const item = await io.todos.add({
        title: value,
        completed: false
      });
      commit("put", item);
    },

    async toggleCompleted({
      commit,
      state
    }, item) {
      if (!item) {
        return;
      }
      item.completed = !item.completed;
      const edited = await io.todos.edit(item);
      commit("edit", edited);
    },

    startEdit({
      commit,
      state
    },
      item) {
      state.beforeEditCache = item.title;
      state.editingItem = item;
    },

    async doneEdit({
      commit,
      state
    },
      item) {
      if (!state.editingItem) {
        return;
      }

      if (item.title.trim() == state.beforeEditCache) {
        state.editingItem = null;
        return;
      }

      item.title = item.title.trim();
      if (!item.title) {
        await io.todos.remove(item);
        commit("remove", item);
      } else {
        const edited = await io.todos.edit(item);
        commit("edit", edited);
      }
      state.editingItem = null;
    },

    cancelEdit({
      commit,
      state
    },
      item) {
      item.title = this.beforeEditCache;
      state.editingItem = null;
      this.beforeEditCache = "";
    },

    async remove({
      commit
    }, item) {
      await io.todos.remove(item);
      commit("rm", item);
    },

    removeCompleted({
      commit,
      state,
    }) {
      state.items.forEach(async element => {
        if (element.completed) {
          await io.todos.remove(element);
          commit("rm", element);
        }
      });
    },

    setAllDone({
      commit,
      state
    }) {
      state.items.forEach(async element => {
        if (!element.completed) {
          element.completed = true;
          const edited = await io.todos.edit(element);
          commit("edit", edited);
        }
      });
    }

  }

}
