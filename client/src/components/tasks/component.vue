<template>
  <section class="container-flex">
    <!-- Header / Add new task -->
    <header class="card card bg-light mx-1 my-2">
      <div class="card-body py-2">
        <div class="input-group">
          <div class="input-group-prepend">
            <category-selector
              :selected="category(newTask.category)"
              v-on:selected="categorySelected(newTask, $event)"
            />
          </div>
          <input
            class="form-control input-group-append"
            autofocus
            autocomplete="off"
            v-model="newTask.title"
            v-cloak
            @keyup.enter="addNewTask()"
            placeholder="What needs to be done?"
            id="new-task-input"
          />
          <button
            class="btn btn-success input-group-append"
            @click="addNewTask()"
          ><i class="fa fa-plus"></i></button>
        </div>
      </div>
    </header>
    <!-- -->

    <section
      class="task-list my-2"
      v-show="tasks.length"
    >
      <ul
        class="task-list"
        v-cloak
      >
        <task
          v-for="task in filteredTasks"
          :key="task.id"
          :task="task"
          :id="'task_'+task.id"
          v-on:edited="editTask"
          v-on:toggle="toggleTask"
        />

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
      ><strong>{{ remainingTasks }}</strong>
        {{ remainingTasks | pluralize }} left</span>
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

      <!-- ALL DONE  -->
      <div>
        <input
          class="toggle"
          type="checkbox"
          v-model="allDone"
        >
        <label class="toggle btn btn-warning">
          <i class="checkmark fa fa-check-double"></i>
          <span class="placeholder">&nbsp;</span>
        </label>
      </div>

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
          <span
            class="badge badge-secondary fill color"
            :class="colorName(task.color)"
          >
            {{categoryName(task.category)}}
          </span>

          <span
            class="badge badge-secondary fill color"
            :class="colorName(task.color)"
            v-if="task.due_date"
          >
            {{task.due_date | formatDate}}
          </span>

          <!-- BUTTONS -->
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
  </section>
</template>

<script>
import moment from 'moment';

import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
import CategorySelector from '../category-selector.vue';
import Task from './task.vue';
// import ArchivedTask from './archived-task.vue';

export default {
  components: {
    CategorySelector,
    Task
  },

  created () {
    this._fetchAndUpdate();
    this.newTask.category = this.selectedCategoryId;
  },

  data () {
    return {
      newTask: {
        title: '',
        category: null
      },
      editngTask: null
    };
  },

  computed: {
    ...mapState('Tasks', {
      tasks: 'items',
      // editingTask: 'editingItem', // TODO: Rm from state
      selectedCategoryId: 'categoryFilter',
      selectedMilestoneId: 'milestoneFilter'
    }),
    ...mapGetters('Tasks', {
      filteredTasks: 'filtered',
      remainingTasks: 'remaining',
      archivedTaks: 'archived',
      colors: 'colors',
      colorName: 'colorName'
    }),
    ...mapGetters('Categories', ['category', 'categoryName']),

    allDone: {
      get: function () {
        return this.remainingTasks === 0;
      },
      set: function (value) {
        console.log('CVVV', value);
        this.$store.dispatch('Tasks/setAllDone');
      }
    },

    selectedCategory () {
      return this.category(this.selectedCategoryId);
    }
  },

  methods: {
    ...mapActions('Tasks', {
      addTask: 'addNew',
      editTask: 'edit',
      toggleTask: 'toggleCompleted',
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
        milestoneId: this.$route.query.milestone ? this.$route.query.milestone : 'all'
      });
      this.newTask.category = this.selectedCategory ? this.selectedCategoryId : null;
    },

    addNewTask () {
      // this.$store.dispatch('Tasks/addNew', this.newTask);
      this.addTask(this.newTask);
      this.newTask = {
        title: '',
        category: this.selectedCategory ? this.selectedCategoryId : null
      };
    }

    // doneEditTask (task) {
    // this.editTask(task);
    // this.editngTask = null;
    // }

  },

  filters: {
    pluralize: function (n) {
      return n === 1 ? 'item' : 'itmes';
    },
    formatDate (date) {
      return moment(new Date(date)).calendar(null, {
        sameDay: '[Today]',
        sameElse (now) {
          return `[${this.fromNow()}], YYYY-MM-DD`;
        }
      });
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
      console.log('selected cat', this.selectedCategory, this.selectedCategoryId);
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/scss/_colors.scss";
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

span {
  &.badge {
    margin: 0 2px;
  }
}

.archived {
  header {
    margin: 8px;
  }
}

@import "@/scss/__category_selector.scss";

.color-palette {
  &.selector {
    width: 96px;
    right: 0px !important;
    .color-selector {
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;

      text-align: center;
      li {
        display: block;
        button {
          margin: 4px;
          width: 48px !important;
          height: 48px !important;
        }
      }
    }
  }
}

.calendar-input {
  display: none;
}

@import "@/scss/__color_tags.scss";

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
