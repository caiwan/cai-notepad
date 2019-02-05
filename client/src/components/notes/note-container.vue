<template>
  <article class="notes form-group">
    <div v-if="editingNote == note">
      <note-editor
        :note="note"
        :isCreating="false"
        v-on:doneEdit="doneEditNote(note)"
        v-on:cancelEdit="cancelEditNote(note)"
        v-on:pinNote="togglePinNote(note)"
        v-on:removeNote="removeNote(note)"
        v-on:archiveNote="toggleArchiveNote(note)"
      >
      </note-editor>
    </div>

    <div v-else>
      <note
        :note="note"
        v-on:editNote="startEditNote(note)"
        v-on:pinNote="togglePinNote(note)"
        v-on:archiveNote="toggleArchiveNote(note)"
        v-on:removeNote="removeNote(note)"
      ></note>
    </div>

    <ul>
      <li>Task</li>
      <li>Task</li>
      <li>Task</li>
      <li>Task</li>
    </ul>

    <!-- todos || tasks goez here -->

  </article>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

import NoteEditor from './editor.vue';
import Note from './note.vue';

export default {
  name: 'note-container',
  components: {
    Note, NoteEditor
  },
  props: ['note'],
  computed: {
    ...mapState('Notes', { editingNote: 'editingItem' })
  },

  methods: {
    ...mapActions('Notes', {
      startEditNote: 'startEdit',
      doneEditNote: 'doneEdit',
      cancelEditNote: 'cancelEdit',
      toggleArchiveNote: 'toggleArchive'
    }),

    removeNote (note) {
      if (confirm('Are you sure?')) {
        if (this.editingNote === note) {
          this.cancelEditNote(note);
        }
        this.$store.dispatch('Notes/remove', note);
      }
    },

    togglePinNote (note) {
      this.$store.dispatch('Notes/togglePin', note);
    },

    startEditNote (note) {
      if (this.isCreateNew) {
        alert('Save new note first // add confirm dialog plz');
        return;
      }
      this.$store.dispatch('Notes/startEdit', note);
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
