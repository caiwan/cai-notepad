import io from '@/services/io';

var _id = 0;

export default {
  namespaced: true,

  state: {
    items: [],
    // uid: 0,
    editingItem: null,
    beforeEditCache: "",
  },

  mutations: {
    clear: (state) => state.items = [],

    put: (state, item) => state.items.push(item),

    putAll: (state, items) => state.items = state.items.concat(items),

    edit: (state, item) => {
      const index = state.items.findIndex((elem) => {
        return elem._id === item._id;
      });
      // we get back a new object, and we need to get setters to be invoked
      var storedItem = state.items[index];
      for (var key in item) {
        if (item.hasOwnProperty(key)) {
          storedItem[key] = item[key];
        }
      }
    },

    rm: (state, item) => state.items.splice(state.items.indexOf(item), 1),

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
      // const items = await io.notes.fetchAll();
      const items = [
        { _id: 1, title: 'hello', content: 'exmaple' },
        { _id: 2, title: 'hello2', content: 'exmaple2' }
      ];
      console.error('Not implemented');
      commit("clear");
      commit("putAll", items);
    },

    async addNew({
      commit,
      state
    }, value) {
      value.title = value.title && value.title.trim();
      value.content = value.content && value.content.trim();
      if (!value.title && !value.content) {
        return;
      }
      // const item = await io.notes.add({
      //   title: value,
      //   completed: false
      // });

      console.error('Not implemented');

      const item = {
        id: _id++,
        ...value
      }

      commit("put", item);
    },

    async togglePin({
      commit
    }, item) {
      console.error('Not implemented');
      // await io.notes.remove(item);
      // commit("rm", item);
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

      // item.title = item.title.trim();
      // if (!item.title) {
      //   await io.notes.remove(item);
      //   commit("remove", item);
      // } else {
      //   const edited = await io.notes.edit(item);
      //   commit("edit", edited);
      // }

      console.error('Not implemented');

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
      // await io.notes.remove(item);
      console.error('Not implemented');
      commit("rm", item);
    },

    async archive({
      commit
    }, item) {
      console.error('Not implemented');
      // await io.notes.remove(item);
      // commit("rm", item);
    },


  }

}
