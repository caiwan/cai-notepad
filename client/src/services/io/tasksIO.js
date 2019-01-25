import { BaseIONode } from './_BaseIONode'

export class Tasks extends BaseIONode {

  constructor(io) {
    super(io)
  }

  fetchAll() {
    return fetch(`${this.root}/tasks/`, {
      credentials: 'same-origin'
    }).then(this.handleFault)
      .then(v => v.json());
  }

  add(task) {
    return fetch(`${this.root}/tasks/`, {
      method: 'POST',
      credentials: 'same-origin',
      ...this.io.toJson(task)
    }).then(this.handleFault)
      .then(v => v.json());
  }

  edit(task) {
    return fetch(`${this.root}/tasks/${task.id}/`, {
      method: 'PUT',
      credentials: 'same-origin',
      ...this.io.toJson(task)
    }).then(this.handleFault)
      .then(v => v.json());
  }

  remove(task) {
    return fetch(`${this.root}/tasks/${task.id}/`, {
      method: 'DELETE',
      credentials: 'same-origin',
    }).then(this.handleFault)
  }
}
