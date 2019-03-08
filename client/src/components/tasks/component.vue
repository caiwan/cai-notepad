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
                class="toggle btn btn-secondary fill color"
                :class="colorName(task.color)"
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
              {{categoryName(task.category)}}
            </span>

            <span
              class="badge badge-secondary color fill"
              v-show="task != editingTask && task.due_date"
              :class="colorName(task.color)"
            >
              {{task.due_date | formatDate}}
            </span>

            <!-- EDIT -->
            <div
              class="input-group"
              v-show="task == editingTask"
            >
              <category-selector
                class="input-group-prepend"
                :selected="category(task.category)"
                v-on:selected="categorySelected(task, $event)"
                v-show="task == editingTask"
              />
              <input
                class="form-control edit-task input-group-append"
                type="text"
                v-model="task.title"
                v-focus="task == editingTask"
                v-show="task == editingTask"
                @keyup.enter="doneEditTask(task)"
                @keyup.esc="cancelEditTask(task)"
              >

              <!-- SCHEDULE  -->
              <datepicker
                v-model="task.due_date"
                :placeholder="'Due date'"
                :format="'yyyy-MM-dd'"
                :bootstrapStyling="true"
                :input-class="'hidden'"
                :clear-button="true"
                :clear-button-icon="'fa fa-backspace'"
                :calendar-button="true"
                :calendar-button-icon="'fa fa-calendar'"
                :calendar-class="'calendar right'"
                :wrapper-class="'calendar-wrapper'"
              />

              <!-- PRIORITY / COLORIZE  -->
              <div class="category color-palette input-group-append">
                <button
                  class="btn btn-outline-secondary outline color"
                  :class="editingTask ? colorName(editingTask.color) : ''"
                  @click="toggleColorPalette()"
                ><i class="fa fa-palette"></i>
                </button>
                <nav
                  class="selector color-palette"
                  v-if="showColorPalette"
                >
                  <ul class="selector-group color-selector">
                    <li
                      v-for="(color, index) in colors"
                      :key="index"
                    >
                      <button
                        class="btn fill color"
                        :class="color.name"
                        @click="selectColor(editingTask, color.value)"
                      ></button>
                    </li>
                  </ul>
                </nav>
              </div>

              <!--SAVE/CANCEL  -->
              <button
                class="btn btn-secondary input-group-append"
                @click="cancelEditTask(task)"
              ><i class=" fa fa-times"></i></button>

              <button
                class="btn btn-success input-group-append"
                @click="doneEditTask(task)"
              ><i class="fa fa-check"></i></button>

            </div>

            <!-- Edit -->
            <button
              v-show="task != editingTask"
              class="btn btn-primary"
              @click="startEditTask(task)"
            ><i class="fa fa-edit"></i></button>

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
    </div>
    <!-- </div> -->
  </section>
</template>

<script>
import moment from 'moment';

import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';
import CategorySelector from '../category-selector.vue';

import Datepicker from 'vuejs-datepicker';

export default {
  components: {
    CategorySelector,
    Datepicker
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
      showColorPalette: false,
      datepickerState: {
        hihlighted: {

        }
      }
    };
  },

  computed: {
    ...mapState('Tasks', {
      tasks: 'items',
      editingTask: 'editingItem',
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
        return this.remaining === 0;
      },
      set: function (value) {
        this.$store.dispatch('Tasks/setAllDone');
      }
    },

    selectedCategory () {
      return this.category(this.selectedCategoryId);
    }
  },

  methods: {
    ...mapActions('Tasks', {
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
      this.$store.dispatch('Tasks/addNew', this.newTask);
      this.newTask = {
        title: '',
        category: this.selectedCategory ? this.selectedCategoryId : null
      };
    },

    startEditTask (task) {
      this.showColorPalette = false;
      this.$store.dispatch('Tasks/startEdit', task);
    },
    doneEditTask (task) {
      this.showColorPalette = false;
      this.$store.dispatch('Tasks/doneEdit', task);
    },

    cancelEditTask (task) {
      this.showColorPalette = false;
      this.$store.dispatch('Tasks/cancelEdit', task);
    },

    categorySelected (task, category) {
      const categoryId = category ? category.id : null;
      console.log('select category', { task, categoryId, category });
      task.category = categoryId;
    },

    toggleColorPalette () {
      this.showColorPalette = !this.showColorPalette;
    },

    selectColor (task, colorId) {
      this.showColorPalette = false;
      task.color = colorId;
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
