import { BaseIONode } from './_BaseIONode';

/* global fetch */

export class Tags extends BaseIONode {
  queryAutocomplete (query, limit) {
    return fetch(`${this.root}/tags/autocomplete/?q=${query}&l=${limit}`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }
}
