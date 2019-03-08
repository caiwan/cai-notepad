export default {
  mutations: {
    clear: (state) => { state.items = []; },

    put: (state, item) => { state.items.push(item); },
    putFront: (state, item) => { state.items.unshift(item); },

    putAll: (state, items) => { state.items = state.items.concat(items); },

    edit: (state, item) => {
      const index = state.items.findIndex((elem) => {
        return elem.id === item.id;
      });
      // we get back a new object, and we need to get setters to be invoked
      let storedItem = state.items[index];
      Object.assign(storedItem, item);
    },

    rm: (state, item) => state.items.splice(state.items.indexOf(item), 1),

    toggle: (state, property) => { state[property] = !state[property]; },
    set: (state, { property, value }) => { state[property] = value; },
    fetchStart: (state) => { state.isLoading = true; },
    fetchEnd: (state) => { state.isLoading = false; }
  }
};
