
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

    let j = null;
    try {
      j = await v.json();
    } catch (e) {
      throw Error(`${v.status} ${v.statusText}`);
    }
    console.error(`Error: ${v.status} ${v.statusText}`, j);
    throw Error(`${j.message}`);
  }
}
