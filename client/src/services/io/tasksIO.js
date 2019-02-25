import { BaseIONode } from './_BaseIONode';

/* global fetch */

export class Tasks extends BaseIONode {
  fetchAll () {
    return fetch(`${this.root}/tasks/`, {
      method: 'GET',
      credentials: 'same-origin',
      headers: this.io.headers
    }).then(this.handleFault)
      .then(v => v.json());
  }

  add (task) {
    return fetch(`${this.root}/tasks/`, {
      method: 'POST',
      credentials: 'same-origin',
      ...this.io.toJson(task)
    }).then(this.handleFault)
      .then(v => v.json());
  }

  edit (task) {
    return fetch(`${this.root}/tasks/${task.id}/`, {
      method: 'PUT',
      credentials: 'same-origin',
      ...this.io.toJson(task)
    }).then(this.handleFault)
      .then(v => v.json());
  }

  remove (task) {
    return fetch(`${this.root}/tasks/${task.id}/`, {
      method: 'DELETE',
      credentials: 'same-origin',
      headers: this.io.headers
    }).then(this.handleFault);
  }
}
