// Does a QnD Shallow copy
export function copyObject (target, source) {
  for (const key in source) {
    if (source.hasOwnProperty(key)) {
      if (typeof source[key] === 'function') continue;
      else if (typeof source[key] === 'object' && target[key] != null) copyObject(target[key], source[key]); // If there's any loop in there, well ...
      // TODO Array?
      else target[key] = source[key];
    }
  }
  return target;
}

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
      var storedItem = state.items[index];
      copyObject(storedItem, item);
    },

    rm: (state, item) => state.items.splice(state.items.indexOf(item), 1),

    toggle: (state, property) => { state[property] = !state[property]; },
    set: (state, { property, value }) => { state[property] = value; },
    fetchStart: (state) => { state.isLoading = true; },
    fetchEnd: (state) => { state.isLoading = false; }
  }
};

// TODO: -> servicess

export class Filter {
  constructor () {
    this.all = (items) => items.filter(item => !item.is_archived);
    this.active = (items) => items.filter(item => !item.is_completed && !item.is_archived);
    this.completed = (items) => items.filter(item => item.is_completed && !item.is_archived);
  }

  _category (items, categoryId) {
    if (categoryId === 'all') {
      return items;
    } else if (categoryId === 'unassigned') {
      return items.filter(item => !item.category);
    } else {
      return items.filter(item => item.category && item.category === categoryId);
    }
  };

  _milestone (items, milestoneId) {
    return items;
  };

  _all (items, milestoneId, categoryId) { return this._category(this._milestone(items, milestoneId), categoryId); }
};
