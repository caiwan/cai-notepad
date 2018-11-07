import { Todos } from './todosIO'
import { Notes } from './notesIO'
import { Tags } from './tagsIO'
import { Categories } from './categoriesIO'

class IO {
  constructor() {
    this.headers = null;
    this.root = './api';

    this.todos = null;
    this.notes = null;
    this.tags = null;

    const data = { csrftoken: "nope" }

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
    this.notes = new Notes(this);
    this.tags = new Tags(this);
    this.categories = new Categories(this);

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
