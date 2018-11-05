<template>
  <section class="card bg-light mx-1 my-2">
    <header class="card-header p-2">
      <input class="form-control" type="text" autofocus autocomplete="off" placeholder="Title" v-model="note.title" />
    </header>
    <!-- text editor goez here -->
    <div class="card-body p-2">
      <textarea id="content" class="form-control" placeholder="Take a note..." v-model="note.content"></textarea>
    </div>
    <!-- footer -->
    <footer class="card-footer p-1">
      <!-- - category | tags -->
      <tag-input :choices="autocomplete" :tags="pTags" />
      <span> + category </span>
      <!-- - other opts buttons -->
      <button @click="done()" class="btn btn-primary btn-raised">Done</button>
      <button @click="cancel()" class="btn btn-primary btn-raised">Cancel</button>
    </footer>
  </section>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
// TODO: we need to finetune this thing: 
import autoResize from 'autoresize-textarea';
import TagInput from '../tag-input.vue'

export default {
  components: {
    TagInput
  },
  props: {
    note: {
      type: [Object],
      required: true,
      default: () => {
        return {
          title: "", content: "", tags: [], category: ""
        }
      }
    }
  },
  data() {
    return {
      pTags: this.note.tags !== undefined ? this.note.tags.slice() : []
    };
  },
  mounted() {
    this._contentEditor = autoResize(this.$el.querySelector("#content"));
  },
  computed: {
    ...mapState("Notes/Tags", { autocompleteTags: "items" })
  },
  methods: {
    autocomplete(tag) {
      if (tag.length < 3) {
        return [];
      }
      this.$store.dispatch("Notes/Tags/queryAutocomplete", tag);
      return this.autocompleteTags;
    },
    done() {
      // this._contentEditor.reset();
      this.note.tags = this.pTags.slice();
      console.log({ tags: this.note.tags });
      this.$emit('doneEdit');
    },
    cancel() {
      // this._contentEditor.reset();
      this.$emit('cancelEdit');
    }
  },
  watch: {

  }
}
</script>

<style>
</style>
