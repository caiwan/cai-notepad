
<template>
  <section class="container-fluid">

    <header class="row">
      <div class="col-12">
        <div v-if="!isCreateNew">
          <section class="card bg-light mx-1 my-2">
            <div class="card-body py-2"><button @click="createNewNote()" class="btn btn-primary btn-raised">New note</button></div>
          </section>
        </div>
        <div v-else>
          <note-editor :note="newNote" v-on:doneEdit="addNewNote()" v-on:cancelEdit="clearNewNote()"></note-editor>
          <!-- todos goez here -->
        </div>
      </div>
    </header>

    <section class="row">
      <div class="col-12">
        <article class="notes form-group" v-for="note in notes" :key="note._id">

          <div class="editor" v-if="editingNote == note">
            <note-editor :note="note" v-on:doneEdit="doneEditNote(note)" v-on:cancelEdit="cancelEditNote(note)">
            </note-editor>
          </div>

          <div class="view" v-else>
            <note :note="note" v-on:editNote="startEditNote(note)" v-on:pinNote="togglePinNote(note)" v-on:removeNote="removeNote(note)"></note>
          </div>

          <!-- todos || tasks goez here -->
        </article>
      </div>
    </section>

  </section>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";

import NoteEditor from './editor.vue';
import Note from './note.vue'

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
</style>
