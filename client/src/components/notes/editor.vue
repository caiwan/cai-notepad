        <template>
  <div class="card bg-light mx-1 my-2">
    <header class="card-header">
      <input
        type="text"
        autofocus
        autocomplete="off"
        placeholder="Title"
        v-model="note.title"
      >
    </header>
    <div class="card-body">
      <textarea
        id="content"
        placeholder="Take a note..."
        v-model="note.content"
        @keydown="__keydown"
      ></textarea>
    </div>
    <!-- footer -->
    <footer class="card-footer">
      <!-- - category | tags -->
      <div class="footer-tagline">
        <i class="fa fa-tags"></i>
        <tag-input
          :choices="autocomplete"
          :tags="pTags"
        />
      </div>
      <div class="footer-bottom-line">
        <!-- CATEGORY SELECTOR  -->
        <category-selector
          :selected="category(note.category)"
          v-on:selected="categorySelected"
        />

        <!-- DATE PICKER  -->
        <datepicker
          v-model="pDate"
          :placeholder="'Due date'"
          :format="'yyyy-MM-dd'"
          :bootstrapStyling="true"
          :input-class="'calendar-input'"
          :clear-button="true"
          :clear-button-icon="'fa fa-backspace'"
          :calendar-button="true"
          :calendar-button-icon="'fa fa-calendar'"
          :calendar-class="'calendar'"
          :wrapper-class="'calendar-wrapper'"
          :bootstrap-styling="true"
        />

        <!-- FOOTER BUTTONS -->
        <button
          @click="pin()"
          class="btn btn-sm btn-primary btn-raised"
        >{{note.is_pinned ? "Unpin" : "Pin"}}</button>
        <button
          v-if="!isCreating"
          @click="archive()"
          class="btn btn-sm btn-primary btn-raised"
        >{{note.is_archived ? "Restore" : "Archive"}}</button>
        <button
          v-if="!isCreating"
          @click="remove()"
          class="btn btn-sm btn-danger btn-raised"
        >Delete</button>
        <span class="gap"></span>
        <button
          @click="done()"
          class="btn btn-sm btn-success btn-raised"
        >Done</button>
        <button
          @click="cancel()"
          class="btn btn-sm btn-secondary btn-raised"
        >Cancel</button>
      </div>
    </footer>
  </div>
</template>

<script>
import autoResize from '@/utils/autoresize-textarea';
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

import TagInput from '../tag-input.vue';
import CategorySelector from '../category-selector.vue';

import Datepicker from 'vuejs-datepicker';

export default {
  components: {
    TagInput,
    Datepicker,
    CategorySelector
  },

  props: {
    note: {
      type: [Object],
      required: true,
      default: () => {
        return {
          title: '',
          content: '',
          tags: [],
          category: ''
        };
      }
    },
    isCreating: { type: Boolean, default: false }
  },

  data () {
    return {
      pDate: this.note.due_date ? new Date(this.note.due_date) : '',
      pTags: this.note.tags !== undefined ? this.note.tags.slice() : [],
      _tab: '    ',
      __textarea: null
    };
  },

  computed: {
    ...mapState('Notes/Tags', { autocompleteTags: 'items' }),
    ...mapGetters('Categories', ['category', 'categoryName'])

  },

  methods: {
    autocomplete (tag) {
      if (tag.length < 3) {
        return [];
      }
      this.$store.dispatch('Notes/Tags/queryAutocomplete', tag);
      return this.autocompleteTags;
    },

    categorySelected (category) {
      const categoryId = category ? category.id : null;
      console.log('select category', { categoryId, category });
      this.note.category = categoryId;
    },

    done () {
      this.note.tags = this.pTags.slice();
      this.$emit('doneEdit');
    },
    cancel () {
      this.$emit('cancelEdit');
    },
    pin () {
      this.$emit('pinNote');
    },
    remove () {
      this.$emit('removeNote');
    },
    archive () {
      this.$emit('archiveNote');
    },

    __keydown (event) {
      const keyCode = event.keyCode || event.which;

      if (keyCode === 9) {
        const tab = this.$data._tab;
        const element = event.target;

        event.preventDefault();
        const start = element.selectionStart;
        const end = element.selectionEnd;

        element.value =
          element.value.substring(0, start) +
          tab +
          element.value.substring(end);

        element.setSelectionRange(start + tab.length, start + tab.length);
      }

      // Save for ctrl + enter
      if (
        keyCode === 13 &&
        (event.getModifierState('Control') || // Win
          event.getModifierState('Meta')) // Mac, 'command' key
      ) {
        this.done();
      }
    }

  },

  watch: {
    pDate () {
      if (this.pDate !== null) {
        this.note.due_date = this.pDate.getTime();
      } else {
        this.note.due_date = null;
      }
    }

  },

  mounted () {
    const el = document.getElementById('content');
    this.$data.__textarea = autoResize(el);
  },

  destroyed () {
    this.$data.__textarea.reset();
  }
};
</script>

<style lang="scss" scoped>
@import "@/scss/_colors.scss";

header {
  padding: 2px 4px !important;
  display: flex;
  input {
    padding: 0px;
    font-size: 14pt;
    flex-grow: 1;
    background-color: $gray-800;
    border: 1px solid $gray-600;
    color: $gray-500;
    border-radius: 4px;
  }
}

div {
  padding: 2px 4px !important;
  &.card-body {
    margin: 0px;
  }
  #content {
    font-family: monospace;
    resize: none;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    padding: 0px;
    font-size: 10pt;
    flex-grow: 1;
    background-color: $gray-800;
    border: 1px solid $gray-600;
    // border-radius: 4px;
    color: $gray-500;
  }
}

@import "@/scss/__tag-input.scss";
@import "@/scss/__category_selector.scss";
@import "@/scss/__color_tags.scss";

footer {
  padding: 2px 8px !important;
  .footer-tagline {
    display: flex;
    overflow: hidden;
    align-items: center;
    justify-items: center;
    padding: 0 4px;
    border: 1px solid $gray-600;
  }
  .footer-bottom-line {
    display: flex;
    // overflow: hidden;
    align-items: center;
    justify-items: center;
    padding: 8px 0;

    .gap {
      flex-grow: 1;
    }

    button {
      margin: 0 0.125em;
    }
  }
}
</style>
