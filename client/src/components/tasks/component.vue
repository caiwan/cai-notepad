<template>
  <section class="container-flex">
    <!-- <div class="row"> -->
    <div class="col-md-12">

      <!-- Header / Add new task -->
      <header class="card card bg-light mx-1 my-2">
        <div class="card-body py-2">
          <div class="input-group">

            <div class="input-group-prepend">
              <category-selector
                :category="newTask.category"
                v-on:selected="categorySelected(newTask, $event)"
              />
            </div>

            <input
              class="form-control add-task"
              autofocus
              autocomplete="off"
              v-model="newTask.title"
              v-cloak
              @keyup.enter="addNewTask()"
              placeholder="What needs to be done?"
              id="new-task-input"
            />
            <div class="input-group-append"> <button
                class="btn btn-success"
                type="button"
                @click="addNewTask()"
              ><i class="fa fa-plus"></i></button></div>
          </div>
        </div>
      </header>
      <!-- -->

      <section
        class="main"
        v-show="tasks.length"
      >
        <ul
          class="task-list"
          v-cloak
        >
          <li
            v-for="task in filteredTasks"
            :key="task.id"
            class="task ui-state-default"
            :class="{completed: task.is_completed}"
            v-cloak
          >

            <div v-show="task != editingTask">
              <input
                class="toggle"
                :id="'check_'+task.id"
                type="checkbox"
                v-model="task.is_completed"
                @click="toggleTask(task)"
              >
              <label
                class="toggle btn btn-success"
                :for="'check_'+task.id"
              >
                <i class="checkmark fa fa-check"></i>
                <span class="placeholder">&nbsp;</span>
              </label>
            </div>

            <!--VIEW -->

            <span
              @dblclick="startEditTask(task)"
              @click="toggleTask(task)"
              class="task-title"
              v-show="task != editingTask"
            >
              {{ task.title }}
            </span>
            <span
              class="badge badge-secondary"
              v-show="task != editingTask"
            >
              {{task.category ? task.category.title : "Unassigned"}}
            </span>

            <!-- EDIT -->
            <div
              class="input-group"
              v-show="task == editingTask"
            >
              <category-selector
                class="input-group-prepend"
                :category="task.category"
                v-on:selected="categorySelected(task, $event)"
                v-show="task == editingTask"
              />
              <input
                class="form-control edit-task input-group-append"
                type="text"
                v-model="task.title"
                v-focus="task == editingTask"
                v-show="task == editingTask"
                @blur="doneEditTask(task)"
                @keyup.enter="doneEditTask(task)"
                @keyup.esc="cancelEditTask(task)"
              >

            </div>
            <!-- DELETE -->

            <button
              class="btn btn-danger"
              @click="removeTask(task)"
            ><i class="fa fa-trash"></i></button>

          </li>
        </ul>
      </section>

      <footer
        class="justify-content-between align-items-center"
        v-show="tasks.length"
        v-cloak
      >
        <span
          class="mr-auto task-count badge badge-secondary"
          v-show="remainingTasks"
        ><strong>{{ remainingTasks }}</strong>{{ remainingTasks | pluralize }} left</span>
        <span class="gap" />

        <button
          href="#"
          class="btn btn-outline-primary"
          @click="setFilterTasks('all')"
        >All</button>
        <button
          href="#"
          class="btn btn-outline-primary"
          @click="setFilterTasks('active')"
        >Active</button>
        <button
          href="#"
          class="btn btn-outline-primary"
          @click="setFilterTasks('completed')"
        >Completed</button>
        <button
          class="btn btn-warning"
          type="button"
          @click="setAllDone()"
        ><i class="fa fa-check-double"></i></button>
        <button
          href="#"
          class="btn btn-danger"
          @click="archiveCompleted()"
        ><i class="fa fa-archive"></i></button>
      </footer>
      <!-- -->

      <!-- Archived tasks -->
      <hr />
      <section
        class="archived"
        v-if="archivedTaks.length"
      >
        <header>Archived</header>
        <ul class="task-list">
          <li
            class="task"
            v-for="task in archivedTaks"
            :key="task.id"
          ><span class="task-title">
              {{task.title}}</span>
            <span class="badge badge-secondary">
              {{task.category ? task.category.title : "Unassigned"}}
            </span>
            <!-- Some button -->
            <button
              class="btn btn-primary"
              @click="toggleArchive(task)"
            > <i class="fa fa-level-up-alt"></i></button>
            <!-- DELETE -->
            <button
              class="btn btn-danger"
              @click="removeTask(task)"
            ><i class="fa fa-trash"></i></button>
          </li>
        </ul>
      </section>
    </div>
    <!-- </div> -->
  </section>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
import CategorySelector from '../category-selector.vue';

export default {
  components: {
    CategorySelector
  },

  created () {
    this._fetchAndUpdate();
    this.newTask.category = this.selectedCategory;
  },

  data () {
    return {
      newTask: {
        title: '',
        category: null
      }
    };
  },

  computed: {
    ...mapState('Tasks', {
      tasks: 'items',
      editingTask: 'editingItem',
      categoryId: 'categoryFilter',
      milestoneId: 'milestoneFilter'
    }),
    ...mapGetters('Tasks', {
      filteredTasks: 'filtered',
      remainingTasks: 'remaining',
      archivedTaks: 'archived'
    }),
    ...mapGetters('Categories', { getCategory: 'getCategory' }),

    allDone: {
      get: function () {
        return this.remaining === 0;
      },
      set: function (value) {
        this.$store.dispatch('Tasks/setAllDone');
      }
    },

    selectedCategory () {
      return this.getCategory(this.categoryId);
    }
  },

  methods: {
    ...mapActions('Tasks', {
      toggleTask: 'toggleCompleted',
      startEditTask: 'startEdit',
      doneEditTask: 'doneEdit',
      cancelEditTask: 'cancelEdit',
      removeTask: 'remove',
      archiveCompleted: 'archiveCompleted',
      setAllDone: 'setAllDone',
      toggleArchive: 'toggleArchive'
    }),

    ...mapMutations('Tasks', {
      setFilterTasks: 'show'
    }),

    async _fetchAndUpdate () {
      await this.$store.dispatch('Tasks/fetchAll');
      this.$store.dispatch('Tasks/updateFilters', {
        categoryId: this.$route.query.category ? this.$route.query.category : 'all',
        milestoneId: this.$route.query.milesonte ? this.$route.query.milesonte : 'all'
      });
    },

    addNewTask () {
      this.$store.dispatch('Tasks/addNew', this.newTask);
      this.newTask = {
        title: ''
        // category: this.selectedCategory
      };
    },

    categorySelected (task, category) {
      task.category = category;
      console.log('select category', { task, category });
    }
  },

  filters: {
    pluralize: function (n) {
      return n === 1 ? 'item' : 'itmes';
    }
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        el.focus();
      }
    }
  },

  updated () {
  },

  watch: {
    $route (to, from) {
      this._fetchAndUpdate();
      this.newTask.category = this.selectedCategory;
      console.log('selected cat', this.selectedCategory, this.categoryId);
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../scss/_colors.scss";
ul {
  &.task-list {
    list-style: none;
    margin: 0px;
    padding: 0px;
    .task {
      margin-top: 4px;
      display: flex;
      align-items: baseline;
      .task-title {
        padding-left: 5px;
        flex-grow: 1;
        overflow: hidden;
      }
      &.completed {
        .task-title {
          text-decoration: line-through;
        }
      }
    }
  }
}

hr {
  // color: white;
  border: 1px solid $gray-700;
}

.archived {
  header {
    margin: 8px;
  }
}

// --- custom toggle / checkmark stuff
.toggle {
  margin: 0px;
  @at-root input {
    &.toggle {
      display: none !important;
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
}
// --- toggle

footer {
  margin: 8px;
  display: flex;
  .gap {
    flex-grow: 1;
  }
  button {
    margin-left: 4px !important;
  }
}
// }
</style>
