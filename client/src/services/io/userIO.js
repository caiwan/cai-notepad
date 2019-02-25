import { BaseIONode } from './_BaseIONode';

/* global fetch */

export class User extends BaseIONode {
  login (username, password) {
    return fetch(`${this.root}/auth/login/`, {
      method: 'POST',
      credentials: 'same-origin',
      ...this.io.toJson({
        username, password
      })
    })
      .then(this.handleFault)
      .then(v => v.json());
  }

  fetchProfile () {
    return fetch(`${this.root}/auth/profile`, {
      method: 'GET',
      credentials: 'same-origin',
      headers: this.io.headers
    }).then(this.handleFault)
      .then(v => v.json());
  }

  logout () {
    return fetch(`${this.root}/auth/logout`, {
      method: 'GET',
      credentials: 'same-origin',
      headers: this.io.headers
    }).then(this.handleFault)
      .then(v => v.json());
  }
}
