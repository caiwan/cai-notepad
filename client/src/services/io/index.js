import { Tasks } from './tasksIO';
import { Notes } from './notesIO';
import { Tags } from './tagsIO';
import { Categories } from './categoriesIO';

// Eslint no-undef exceptions
/* global Headers */
/* global Blob */

class IO {
  constructor () {
    this.headers = null;
    this.root = './api';

    this.tasks = null;
    this.notes = null;
    this.tags = null;

    // this.initialized = fetch('./api/settings/', {
    // credentials: 'same-origin'
    // })
    const dummyFetch = async function () {
      return {
        json () {
          return { csrftoken: '' };
        }
      };
    };

    this.initialized = dummyFetch()
      .then(v => v.json())
      .then(data => {
        this.headers = new Headers({
          'X-CSRFToken': data.csrftoken
        });

        this.tasks = new Tasks(this);
        this.notes = new Notes(this);
        this.tags = new Tags(this);
        this.categories = new Categories(this);
      });
  }
  toJson (data) {
    return {
      body: new Blob([JSON.stringify(data)], { type: 'application/json' }),
      headers: this.headers
    };
  }
}

export default new IO();
