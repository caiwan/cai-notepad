import { BaseIONode } from './_BaseIONode'

export class Todos extends BaseIONode {

  constructor(io) {
    super(io)
  }

  fetchAll() {
    return fetch(`${this.root}/tasks/`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

  add(todo) {
    return fetch(`${this.root}/tasks/`, {
      method: 'POST',
      credentials: 'same-origin',
      ...this.io.toJson(todo)
    })
      .then(v => v.json());
  }

  edit(todo) {
    return fetch(`${this.root}/tasks/${todo._id}/`, {
      method: 'PUT',
      credentials: 'same-origin',
      ...this.io.toJson(todo)
    })
      .then(v => v.json());
  }

  remove(todo) {
    return fetch(`${this.root}/tasks/${todo._id}/`, {
      method: 'DELETE',
      credentials: 'same-origin',
    })
  }
}
