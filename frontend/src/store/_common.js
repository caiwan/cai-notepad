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
    set: (state, { property, value }) => { state[property] = value; }
  },
  actions: {
    pushLoad: ({ dispatch }) => dispatch('UI/pushLoad', {}, { root: true }),
    popLoad: ({ dispatch }) => dispatch('UI/popLoad', {}, { root: true })
  }
};

export function arrayMove (arr, oldIndex, newIndex) {
  while (oldIndex < 0) {
    oldIndex += arr.length;
  }
  while (newIndex < 0) {
    newIndex += arr.length;
  }
  if (newIndex >= arr.length) {
    var k = newIndex - arr.length + 1;
    while (k--) {
      arr.push(undefined);
    }
  }
  arr.splice(newIndex, 0, arr.splice(oldIndex, 1)[0]);
  return arr; // for testing purposes
};
