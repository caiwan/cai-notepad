import { BaseIONode } from './_BaseIONode';

/* global fetch */

export class Notes extends BaseIONode {
  fetchAll () {
    return fetch(`${this.root}/notes/`, {
      credentials: 'same-origin'
    }).then(this.handleFault)
      .then(v => v.json());
  }

  add (item) {
    return fetch(`${this.root}/notes/`, {
      method: 'POST',
      credentials: 'same-origin',
      ...this.io.toJson(item)
    }).then(this.handleFault)
      .then(v => v.json());
  }

  edit (item) {
    return fetch(`${this.root}/notes/${item.id}/`, {
      method: 'PUT',
      credentials: 'same-origin',
      ...this.io.toJson(item)
    }).then(this.handleFault)
      .then(v => v.json());
  }

  remove (item) {
    return fetch(`${this.root}/notes/${item.id}/`, {
      method: 'DELETE',
      credentials: 'same-origin'
    }).then(this.handleFault);
  }
}
