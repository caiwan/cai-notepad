// drag-tree.vue
const findRoot = which => {
  let ok = false;
  let that = which;
  while (!ok) {
    if (that.$options._componentTag !== 'drag-node') {
      ok = true;
      break;
    }
    that = that.$parent;
  }
  return that;
};

/**
 */
const hasInclude = (from, to) => {
  return from.$parent._uid === to._uid;
};

/**
 */
const isLinealRelation = (from, to) => {
  let parent = from.$parent;
  let ok = false;
  let status = false;
  while (!ok) {
    if (parent._uid === to._uid) {
      ok = true;
      status = true;
      continue;
    }
    if (
      !parent.$options._componentTag ||
      parent.$options._componentTag === 'drag-tree'
    ) {
      ok = true;
      break;
    }
    parent = parent.$parent;
  }

  return status;
};

/**
 *
 * @param rootCom drag-tree.vue
 * @param from Vnode
 * @param to Vnode
 */
const exchangeData = (rootCom, from, to) => {
  // return;

  // TODO: ...

  if (from._uid === to._uid) {

  }

  const newFrom = from.model;
  // const newFrom = Object.assign({}, from.model);
  if (hasInclude(from, to)) {
    const tempParent = to.$parent;
    const toModel = to.model;

    if (tempParent.$options._componentTag !== 'drag-node') {
      tempParent.newData.push(newFrom);
      toModel.children = toModel.children.filter(item => item.id !== newFrom.id);
      return;
    }

    const toParentModel = tempParent.model;
    toModel.children = toModel.children.filter(item => item.id !== newFrom.id);
    toParentModel.children = toParentModel.children.concat([newFrom]);
    return;
  }

  if (isLinealRelation(from, to)) {
    const fromParentModel = from.$parent.model;
    const toModel = to.model;

    fromParentModel.children = fromParentModel.children.filter(
      item => item.id !== newFrom.id
    );

    toModel.children = toModel.children.concat([newFrom]);
    return;
  }

  const fromParentModel = from.$parent.model;
  const toModel = to.model;
  // from
  if (from.$parent.$options._componentTag !== 'drag-node') {
    from.$parent.newData = from.$parent.newData.filter(
      item => item.id !== newFrom.id
    );
  } else {
    fromParentModel.children = fromParentModel.children.filter(
      item => item.id !== newFrom.id
    );
  }

  if (!toModel.children) {
    toModel.children = [newFrom];
  } else {
    toModel.children = toModel.children.concat([newFrom]);
  }
};

export { findRoot, exchangeData };
