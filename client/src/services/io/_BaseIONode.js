
/* global Error */

export class BaseIONode {
  constructor (io) {
    this.io = io;
  }

  get root () {
    return this.io.root;
  }

  get headers () {
    return this.io.headers;
  }

  async handleFault (v) {
    if (v.ok) { return v; }
    const j = await v.json();
    console.error(`Error: ${v.status} ${v.statusText} ${j.message}`);
    throw Error(`${j.message}`);
  }
}
