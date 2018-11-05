import { BaseIONode } from './_BaseIONode'

export class Tags extends BaseIONode {
  constructor(io) {
    super(io)
  }
  queryAutocomplete(query, limit) {
    return fetch(`${this.root}/tags/autocomplete/?q=${query}&l=${limit}`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

}
