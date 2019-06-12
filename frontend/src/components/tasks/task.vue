<template>
  <li class="task ui-state-default" :class="{completed: task.is_completed}" v-cloak>
    <!--VIEW -->
    <template v-if="!isEditing">
      <div>
        <input
          class="toggle"
          :id="'check_'+task.id"
          type="checkbox"
          v-model="task.is_completed"
          @click="toggle"
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

      <span @dblclick="startEdit" @click="toggle" class="task-title">{{ task.title }}</span>
      <span class="badge badge-secondary">{{categoryName(task.category)}}</span>

      <span
        class="badge badge-secondary color fill"
        v-show="task.due_date"
        :class="colorName(task.color)"
      >{{task.due_date | formatDate}}</span>
    </template>

    <!-- EDIT -->
    <template v-else>
      <div class="input-group">
        <category-selector
          class="input-group-prepend"
          :selected="category(editingTask.category)"
          v-on:selected="categorySelected"
          v-show="isEditing"
        />
        <input
          class="form-control edit-task input-group-append"
          type="text"
          v-model="editingTask.title"
          v-focus="isEditing"
          v-show="isEditing"
          @keyup.enter="doneEdit"
          @keyup.esc="cancelEdit"
        >

        <!-- SCHEDULE  -->
        <datepicker
          v-model="pDate"
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
        <!-- TODO: Move it to its very own component to reuse it somwehere else-->
        <div class="category color-palette input-group-append">
          <button
            class="btn btn-outline-secondary outline color"
            :class="editingTask ? colorName(editingTask.color) : ''"
            @click="toggleColorPalette"
          >
            <i class="fa fa-palette"></i>
          </button>
          <nav class="selector color-palette" v-if="showColorPalette">
            <ul class="selector-group color-selector">
              <li v-for="(color, index) in colors" :key="index">
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
        <button class="btn btn-secondary input-group-append" @click="cancelEdit">
          <i class="fa fa-times"></i>
        </button>

        <button class="btn btn-success input-group-append" @click="doneEdit">
          <i class="fa fa-check"></i>
        </button>
      </div>
    </template>

    <!-- Enter edit mode -->
    <button v-show="!isEditing" class="btn btn-primary" @click="startEdit()">
      <i class="fa fa-edit"></i>
    </button>

    <!-- DELETE -->
    <button class="btn btn-danger" @click="removeTask">
      <i class="fa fa-trash"></i>
    </button>
  </li>
</template>

<script>
import Datepicker from 'vuejs-datepicker';

import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

import { formatFuzzyDate } from '@/utils';

import CategorySelector from '../category-selector.vue';

export default {
  name: 'task',

  props: {
    task: { type: Object, required: true }
  },

  components: {
    CategorySelector,
    Datepicker
  },

  data () {
    return {
      pDate: this.task.due_date ? new Date(this.task.due_date * 1000) : '',
      pTask: this.task,
      editingTask: null,
      showColorPalette: false,
      datepickerState: {
        highlighted: {}
      }
    };
  },

  computed: {
    ...mapGetters('Tasks', {
      colors: 'colors',
      colorName: 'colorName'
    }),
    ...mapGetters('Categories', ['category', 'categoryName']),

    selectedCategory () {
      return this.category(this.selectedCategoryId);
    },

    isEditing () {
      return !!this.editingTask;
    }
  },

  methods: {
    startEdit () {
      this.showColorPalette = false;
      this.editingTask = Object.assign({}, this.task);
    },

    doneEdit () {
      this.showColorPalette = false;
      this.$emit('edited', this.editingTask);
      this.editingTask = null;
    },

    toggle () {
      this.$emit('toggle', this.task);
    },

    cancelEdit () {
      this.showColorPalette = false;
      this.editingTask = null;
    },

    categorySelected (category) {
      const categoryId = category ? category.id : null;
      console.log('select category', {
        task: this.editingTask,
        categoryId,
        category
      });
      this.editingTask.category = categoryId;
    },

    toggleColorPalette () {
      this.showColorPalette = !this.showColorPalette;
    },

    selectColor (task, colorId) {
      this.showColorPalette = false;
      task.color = colorId;
    },

    removeTask () {
      this.$emit('remove', this.task);
      this.showColorPalette = false;
      this.editingTask = null;
    }
  },

  filters: {
    formatDate: date => formatFuzzyDate(date)
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        el.focus();
      }
    } //
  },

  watch: {
    pDate () {
      this.editingTask.due_date = this.pDate
        ? this.pDate.getTime() / 1000
        : null;
    } //
  }
};
</script>

<style lang="scss" scoped>
@import "@/scss/_colors.scss";
li {
  &.task {
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

span {
  &.badge {
    margin: 0 2px;
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
</style>
