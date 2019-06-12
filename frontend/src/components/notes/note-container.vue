<template>
  <article class="notes form-group">
    <div v-if="isEditing">
      <note-editor
        :note="editingNote"
        :isCreating="false"
        v-on:doneEdit="doneEditNote"
        v-on:cancelEdit="cancelEditNote"
        v-on:pinNote="togglePinNote"
        v-on:removeNote="removeNote"
        v-on:archiveNote="toggleArchiveNote"
      ></note-editor>
    </div>

    <div v-else>
      <note
        :note="note"
        v-on:editNote="startEditNote"
        v-on:pinNote="togglePinNote"
        v-on:archiveNote="toggleArchiveNote"
        v-on:removeNote="removeNote"
      ></note>
    </div>

    <!-- <ul>
      <li>Task</li>
      <li>Task</li>
      <li>Task</li>
      <li>Task</li>
    </ul>-->

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
    Note,
    NoteEditor
  },
  props: ['note', 'editingNote'],
  computed: {
    isEditing () {
      return this.editingNote && this.editingNote.id === this.note.id;
    }
  },

  methods: {
    // ...mapActions('Notes', {
    // toggleArchiveNote: 'toggleArchive'
    // }),

    removeNote () {
      if (confirm('Are you sure?')) {
        if (this.isEditing) {
          this.cancelEditNote();
        }
        this.$store.dispatch('Notes/remove', this.note);
      }
    },

    togglePinNote () {
      this.$store.dispatch('Notes/togglePin', this.note);
    },
    toggleArchiveNote () {
      this.$store.dispatch('Notes/toggleArchive', this.note);
    },

    startEditNote () {
      this.$emit('startEdit', this.note);
    },
    doneEditNote () {
      this.$emit('doneEdit');
    },
    cancelEditNote () {
      this.$emit('cancelEdit');
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
