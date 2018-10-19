class BaseIONode {
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

class Todos extends BaseIONode {

  constructor(io) {
    super(io)
    // this.uid = 0;
  }

  fetchAll() {
    return fetch(`${this.root}/tasks/`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

  add(todo) {
    return fetch(`${this.root}/tasks/`, {
      method: 'POST',
      credentials: 'same-origin',
      ...this.io.toJson(todo)
    })
      .then(v => v.json());
  }

  edit(todo) { 
    return fetch(`${this.root}/tasks/${todo._id}/`, {
      method: 'PUT',
      credentials: 'same-origin',
      ...this.io.toJson(todo)
    })
      .then(v => v.json());
  }

  remove(todo) { 
    return fetch(`${this.root}/tasks/${todo._id}/`, {
      method: 'DELETE',
      credentials: 'same-origin',
    })
  }
}

class IO {
  constructor() {
    this.headers = null;
    this.root = './api';

    this.todos = null;

    const data = {csrftoken:"nope"}

    // this.initialized = fetch('./api/settings/', {
    // credentials: 'same-origin'
    // })
    // .then(v => v.json())
    // .then(data =>{
    // this.root = `${data.root}/api`;

    this.headers = new Headers({
     'X-CSRFToken': data.csrftoken
    });

    this.todos = new Todos(this);

    // })
  }
  toJson(data) {
    return {
      body: new Blob([JSON.stringify(data)], { type: 'application/json' }),
      headers: this.headers
    };
  }
}

export default new IO();
