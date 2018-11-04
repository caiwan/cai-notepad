
export default {
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
  }
};
