<template>
  <section class="container-flex">
    <!-- Header / Add new task -->
    <header class="card card bg-light mx-1 my-2">
      <div class="card-body py-2">
        <div class="input-group">
          <div class="input-group-prepend">
            <category-selector
              :selected="category(newTask.category)"
              v-on:selected="newTaskCategorySelected"
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
      class="task-list"
      v-if="tasks.length"
    >
      <ul v-cloak>
        <task
          v-for="task in filteredTasks"
          :key="task.id"
          :task="task"
          :id="'task_'+task.id"
          v-on:edited="editTask"
          v-on:toggle="toggleTask"
          v-on:remove="removeTask"
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
    <!-- TODO: move to separate component -->
    <hr />
    <section
      class="archived"
      v-if="archivedTaks.length"
    >
      <header>Archived</header>
      <section class="task-list">
        <ul>
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
    this._fetchAndUpdate(this.$route);
  },

  data () {
    return {
      newTask: {
        title: '',
        category: null
      },
      editngTask: null,
      lastSelectedCategory: null
    };
  },

  computed: {
    ...mapState('Tasks', {
      tasks: 'items',
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
        console.log('toggle all', value);
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

    async _fetchAndUpdate (route) {
      this.$store.dispatch('Tasks/updateFilters', {
        categoryId: route.query.category ? route.query.category : 'all',
        milestoneId: route.query.milestone ? route.query.milestone : 'all'
      });
      await this.$store.dispatch('Tasks/fetchAll');
      const self = this;
      setTimeout(() => {
        self.lastSelectedCategory = self.selectedCategory ? self.selectedCategory.id : null;
        self.newTask.category = self.lastSelectedCategory;
        console.log('filtering', self.selectedCategory, self.selectedCategoryId);
      });
    },

    addNewTask () {
      this.addTask(this.newTask);
      this.newTask = {
        title: '',
        category: this.lastSelectedCategory

      };
    },

    newTaskCategorySelected (category) {
      const categoryId = category ? category.id : null;
      console.log('select category', { categoryId, category });
      this.newTask.category = categoryId;
      this.lastSelectedCategory = categoryId;
    }
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
      this._fetchAndUpdate(to);
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/scss/_colors.scss";
.task-list {
  margin: 4px;
  ul {
    list-style: none;
    margin: 0px;
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
