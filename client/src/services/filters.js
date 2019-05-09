export default {
  all: (items) => items.filter(item => !item.is_archived),
  active: (items) => items.filter(item => !item.is_completed && !item.is_archived),
  completed: (items) => items.filter(item => item.is_completed && !item.is_archived)
};
