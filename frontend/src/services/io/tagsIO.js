import { BaseIONode } from './_BaseIONode';

/* global fetch */

export class Tags extends BaseIONode {
  queryAutocomplete (query, limit) {
    return fetch(`${this.root}/tags/autocomplete/?q=${query}&l=${limit}`, {
      method: 'GET',
      credentials: 'same-origin',
      headers: this.io.headers
    })
      .then(v => v.json());
  }
}
