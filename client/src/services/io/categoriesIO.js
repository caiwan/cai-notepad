import { BaseIONode } from './_BaseIONode'

export class Categories extends BaseIONode {
  constructor(io) {
    super(io)
  }
  fetchAll() {
    return fetch(`${this.root}/categories/`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

  add(item) {
    return fetch(`${this.root}/categories/`, {
      method: 'POST',
      credentials: 'same-origin',
      ...this.io.toJson(item)
    })
      .then(v => v.json());
  }

  edit(item) {
    return fetch(`${this.root}/categories/${item._id}/`, {
      method: 'PUT',
      credentials: 'same-origin',
      ...this.io.toJson(item)
    })
      .then(v => v.json());
  }

  remove(item) {
    return fetch(`${this.root}/categories/${item._id}/`, {
      method: 'DELETE',
      credentials: 'same-origin',
    })
  }
}
