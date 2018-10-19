export class BaseIONode {
  constructor(io) {
    this.io = io;
  }

  get root() {
    return this.io.root;
  }

  get headers() {
    return this.io.headers;
  }
}
