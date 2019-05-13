<template>
  <section class="card bg-light mx-1 my-2">
    <header class="card-header note-title-row">
      <span @dblclick="edit()">{{ note.title }}&nbsp;</span>
      <button
        class="btn btn-sm btn-danger"
        @click="remove()"
      ><i class="fa fa-trash"></i></button>
      <button
        class="btn btn-sm btn-warning"
        @click="edit()"
      ><i class="fa fa-edit"></i></button>
      <button
        class="btn btn-sm btn-primary"
        @click="archive()"
      ><i class="fas fa-archive"></i></button>
      <button
        class="btn btn-sm btn-primary"
        @click="pin()"
      ><i class="fas fa-bookmark"></i></button>
    </header>
    <section class="card-body p-2 m-0">
      <vue-markdown :source="note.content"></vue-markdown>
    </section>
    <footer class="card-footer p-2">

      <div
        class="footer-tagline"
        v-if="note.tags.length"
      >
        <i class="fa fa-tags"></i>
        <ul class="tags">
          <li
            v-for="tag in note.tags"
            :key="tag"
            class="tag"
          >{{tag}}</li>
        </ul>
      </div>
      <i class="fa fa-folder"></i>
      &nbsp;
      {{categoryName(note.category)}}
      &nbsp;
      <template v-if="note.due_date">
        <i class="fa fa-calendar"></i>
        &nbsp;
        {{note.due_date | formatDate}}
      </template>
    </footer>
  </section>

</template>

<script>
import moment from 'moment';
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

export default {
  props: ['note'],
  computed: {
    ...mapGetters('Categories', ['category', 'categoryName'])
  },
  methods: {
    edit () {
      this.$emit('editNote');
    },
    remove () {
      this.$emit('removeNote');
    },
    pin () {
      this.$emit('pinNote');
    },
    archive () {
      this.$emit('archiveNote');
    }
  },
  filters: {
    formatDate (date) {
      return moment(new Date(date)).format('YYYY-MM-DD');
    }
  }
};
</script>

<style lang="scss" rel="stylesheet/scss">
@import "../../scss/_tag-input.scss";
header {
  &.note-title-row {
    display: flex;
    overflow: hidden;
    align-items: center;
    justify-items: center;
    padding: 2px 8px !important;
    span {
      flex-grow: 1;
      font-size: 14pt;
    }
    button {
      margin: 0 0.125em;
      width: 28px;
      height: 28px;
    }
  }
}

footer {
  .footer-tagline {
    display: flex;
    overflow: hidden;
    align-items: center;
    justify-items: center;
    padding: 0 4px;
    // border: 1px solid $gray-600;
  }
}
</style>
