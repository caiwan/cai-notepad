<template>
  <section class="container-fluid">

    <header>
      <div :class="{hide : isCreateNew}">
        <button @click="createNewNote()" class="btn btn-primary btn-raised">New note</button></div>
      <div :class="{hide : !isCreateNew}">
        <note-editor :note="newNote" v-on:doneEdit="addNewNote()" v-on:cancelEdit="clearNewNote()"></note-editor>
        <!-- todos goez here -->
      </div>
    </header>

    <section>
      <article class="notes form-group" v-for="note in notes" :key="note._id">
        <div class="view" :class="{editing : editingNote == note}">
          <note :note="note" v-on:editNote="startEditNote(note)" v-on:pinNote="togglePinNote(note)" v-on:removeNote="removeNote(note)"></note>
        </div>
        <div class="editor" :class="{editing : editingNote == note}">
          <note-editor :note="note" v-on:doneEdit="doneEditNote(note)" v-on:cancelEdit="cancelEditNote(note)">
          </note-editor>
        </div>
        <!-- todos || tasks goez here -->
      </article>
    </section>

  </section>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";

import NoteEditor from './note/editor.vue';
import Note from './note/note.vue'

export default {
  name: "notes",
  components: {
    Note, NoteEditor
  },
  created() {
    this.$store.dispatch("Notes/fetchAll");
  },
  data() {
    return {
      isCreateNew: false,
      newNote: {
        title: '',
        content: ''
      }
    };
  },
  computed: {
    ...mapState("Notes", { notes: "items", editingNote: "editingItem" }),
  },
  methods: {
    ...mapActions("Notes", {
      startEditNote: "startEdit",
      doneEditNote: "doneEdit",
      cancelEditNote: "cancelEdit",
      removeNote: "remove",
      togglePinNote: "togglePin"
    }),

    startEditNote(note) {
      if (this.isCreateNew) {
        alert('Save new note first // add confirm dialog plz');
        return;
      }
      this.$store.dispatch("Notes/startEdit", note);
    },

    createNewNote() {
      if (this.editingNote) {
        alert('Save editing note first // add confirm dialog plz');
        return;
      }
      this.isCreateNew = true;
    },
    clearNewNote() {
      this.newNote = {
        title: '', content: ''
      };
      this.isCreateNew = false;
    },
    addNewNote() {
      this.$store.dispatch("Notes/addNew", this.newNote);
      this.clearNewNote();
    }
  }
};
</script>

<style lang="scss">
.hide {
  display: none !important;
}
.notes {
  .view {
    // display: block;
    &.editing {
      display: none !important;
    }
  }
  .editor {
    display: none;
    &.editing {
      display: block !important;
    }
  }
}
</style>
