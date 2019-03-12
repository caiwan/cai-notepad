const findRoot = which => {
  let node = which;
  while (node.$parent) {
    if (node.$options._componentTag !== 'drag-node') { return node; }
    node = node.$parent;
  }
  return null;
};

export { findRoot };
