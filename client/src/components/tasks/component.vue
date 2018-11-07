<template>

  <section class="todoapp container">
    <div class="row">
      <div class="col-md-12">
        <!-- -->
        <header>
          <h1>Todos</h1>
          <div class="input-group">
            <div class="input-group-prepend"><button class="btn btn-warning" type="button" @click="setAllDone()"><i class="fa fa-clipboard"></i></button></div>
            <input class="form-control add-todo" autofocus autocomplete="off" v-model="newTodo" @keyup.enter="addNewTodo()" placeholder="What needs to be done?" />
            <div class="input-group-append"> <button class="btn btn-success" type="button" @click="addNewTodo()"><i class="fa fa-plus"></i></button></div>
          </div>
        </header>
        <!-- -->
        <section class="main" v-show="todos.length" v-cloak>
          <ul class="todo-list list-unstyled">
            <li v-for="todo in filteredTodos" :key="todo._id" class="todo ui-state-default" :class="{completed: todo.completed, editing: todo == editingTodo}">
              <div class="view justify-content-between align-items-center" v-show="todos.length" v-cloak>
                <input class="toggle" :id="'check_'+todo._id" type="checkbox" v-model="todo.completed" @click="toggleTodo(todo)">
                <label class="toggle btn btn-success" :for="'check_'+todo._id">
                  <i class="checkmark fa fa-check"></i>
                  <span class="placeholder">&nbsp;</span>
                </label>
                <label class="todo-title" @dblclick="startEditTodo(todo)" :for="'check_'+todo._id">{{ todo.title }} </label>
                <button class="ml-auto btn btn-danger destroy" @click="removeTodo(todo)"><i class="fa fa-trash"></i></button>
              </div>
              <div class="edit">
                <input class="form-control edit-todo" type="text" v-model="todo.title" v-focus="todo == editingTodo" @blur="doneEditTodo(todo)" @keyup.enter="doneEditTodo(todo)" @keyup.esc="cancelEditTodo(todo)">
              </div>
            </li>
          </ul>
        </section>
        <!-- -->
        <footer class="justify-content-between align-items-center" v-show="todos.length" v-cloak>
          <span class="mr-auto todo-count badge badge-secondary" v-show="remainingTodos"><strong>{{ remainingTodos }}</strong>{{ remainingTodos | pluralize }} left</span>
          <a href="#" class="btn btn-outline-primary" @click="setFilterTodos('all')">All</a>
          <a href="#" class="btn btn-outline-primary" @click="setFilterTodos('active')">Active</a>
          <a href="#" class="btn btn-outline-primary" @click="setFilterTodos('completed')">Completed</a>
          <a href="#" class="btn btn-danger" @click="removeCompleted()">Clear completed</a>
        </footer>
        <!-- -->
      </div>
    </div>
  </section>

</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";

export default {
  created() {
    this.$store.dispatch("todos/fetchAll", this.newTodo);
  },

  data() {
    return {
      newTodo: ""
    };
  },

  computed: {
    ...mapState("todos", { todos: "items", editingTodo: "editingItem" }),
    ...mapGetters("todos", {
      filteredTodos: "filtered",
      remainingTodos: "remaining"
    }),

    allDone: {
      get: function () {
        return this.remaining === 0;
      },
      set: function (value) {
        this.$store.dispatch("todos/setAllDone");
      }
    }
  },

  methods: {
    ...mapActions("todos", {
      toggleTodo: "toggleCompleted",
      startEditTodo: "startEdit",
      doneEditTodo: "doneEdit",
      cancelEditTodo: "cancelEdit",
      removeTodo: "remove",
      removeCompleted: "removeCompleted",
      setAllDone: "setAllDone"
    }),

    ...mapMutations("todos", {
      setFilterTodos: "show"
    }),

    addNewTodo() {
      this.$store.dispatch("todos/addNew", this.newTodo);
      this.newTodo = "";
    }
  },

  filters: {
    pluralize: function (n) {
      return n === 1 ? "item" : "itmes";
    }
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        el.focus();
      }
    }
  }
};
</script>

<style lang="scss">
.todoapp {
  // header {
  // }
  section {
    &.main {
      .todo-list {
        .todo {
          margin-top: 4px;
          &.completed {
            .view {
              .todo-title {
                text-decoration: line-through;
              }
            }
          }
          &.editing {
            .view {
              display: none !important;
            }
            .edit {
              display: flex !important;
            }
          }
          .edit {
            display: none;
          }
          .view {
            display: flex;
            .todo-title {
              padding-left: 5px;
            }
          }
        }
        // --- custom toggle / checkmark stuff
        .toggle {
          margin: 0px;
          @at-root input {
            display: none;
            & + label {
              .checkmark {
                display: none;
              }
              .placeholder {
                display: inline-block;
                width: 16px;
              }
            }
            &:checked + label {
              .checkmark {
                display: inline-block !important;
              }
              .placeholder {
                display: none !important;
              }
            }
          }
        }
        // ---
      }
    }
  }
  footer {
    display: flex;
    a {
      &.btn {
        // background-color: indianred;
        margin-left: 4px !important;
      }
    }
  }
}

[v-cloak] {
  display: none;
}
</style>

