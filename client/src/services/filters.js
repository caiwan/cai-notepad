export default {

  all: (items) => items.filter(item => !item.is_archived),
  active: (items) => items.filter(item => !item.is_completed && !item.is_archived),
  completed: (items) => items.filter(item => item.is_completed && !item.is_archived),

  _category (items, categoryId) {
    if (categoryId === 'all') {
      return items;
    } else if (categoryId === 'unassigned') {
      return items.filter(item => !item.category);
    } else {
      return items.filter(item => item.category && item.category === categoryId);
    }
  },

  _milestone (items, milestoneId) {
    return items;
  },

  filter (items, milestoneId, categoryId) { return this._category(this._milestone(items, milestoneId), categoryId); }
};
