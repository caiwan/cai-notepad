<template>
  <section class="main container-flex">
    <!-- <div class="row"> -->
    <div class="col-md-12">
      <header>
        <div v-if="!isCreateNew">
          <section class="card bg-light mx-1 my-2">
            <div class="card-body py-2">
              <button
                @click="createNewNote()"
                class="btn btn-primary btn-raised"
              >New note</button></div>
          </section>
        </div>
        <div v-else>
          <note-editor
            :note="newNote"
            :isCreating="true"
            v-on:doneEdit="addNewNote()"
            v-on:cancelEdit="clearNewNote()"
          ></note-editor>
        </div>
      </header>
      <!-- </div> -->
    </div>

    <!-- PINNED NOTES -->
    <section
      class=""
      v-show="hasPinned"
    >
      <div class="col-12">
        <header>Pinned</header>
        <note-container
          v-for="note in pinnedNotes"
          :key="note.id"
          :note="note"
        />
      </div>
    </section>
    <!-- DEFAULT -->

    <section class="col-12">
      <header v-show="hasOthers && (hasArchived || hasPinned)">Others</header>
      <note-container
        v-for="note in notes"
        :key="note.id"
        :note="note"
      />
    </section>
    <!-- ARCHIVED -->
    <section class="col-12">
      <header v-show="hasArchived">Archived</header>
      <note-container
        v-for="note in archivedNotes"
        :key="note.id"
        :note="note"
      />
    </section>
  </section>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

import NoteEditor from './editor.vue';
import NoteContainer from './note-container.vue';

export default {
  name: 'notes',

  components: {
    NoteContainer, NoteEditor
  },

  created () {
    this._fetchAndUpdate();
  },

  data () {
    return {
      isCreateNew: false,
      newNote: {
        title: '',
        content: '',
        is_pinned: false,
        category: null
      }
    };
  },

  computed: {
    ...mapGetters('Notes', { notes: 'defaultItems', pinnedNotes: 'pinnedItems', archivedNotes: 'archivedItems' }),
    ...mapState('Notes', { categoryId: 'categoryFilter', milestoneId: 'milestoneFilter' }),
    ...mapGetters('Categories', { getCategory: 'getCategory' }),
    hasPinned: () => this.pinnedNotes && this.pinnedNotes.length,
    hasOthers: () => this.notes && this.notes.length,
    hasArchived: () => this.archivedItems && this.archivedItems.length,

    selectedCategory () {
      return this.getCategory(this.categoryId);
    }
  },

  methods: {
    async _fetchAndUpdate () {
      await this.$store.dispatch('Notes/fetchAll');
      this.$store.dispatch('Notes/updateFilters', {
        categoryId: this.$route.query.category ? this.$route.query.category : 'all',
        milestoneId: this.$route.query.milesonte ? this.$route.query.milesonte : 'all'
      });
    },

    createNewNote () {
      if (this.editingNote) {
        alert('Save editing note first // add confirm dialog plz');
        return;
      }
      this.newNote.category = this.selectedCategory;
      this.isCreateNew = true;
    },

    clearNewNote () {
      this.newNote = {
        title: '', content: '', category: this.selectedCategory
      };
      this.isCreateNew = false;
    },

    async addNewNote () {
      this.$store.dispatch('Notes/addNew', this.newNote);
      this.clearNewNote();
    }
  },

  watch: {
    $route (to, from) {
      this._fetchAndUpdate(this);
    }
  }

};
</script>

<style lang="scss" scoped>
</style>
