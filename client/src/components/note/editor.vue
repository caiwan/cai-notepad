<template>
  <section class="card bg-light mx-1 my-2">
    <header class="card-header p-2">
      <input class="card-header form-control" type="text" autofocus autocomplete="off" placeholder="Title" v-model="note.title" />
    </header>
    <!-- text editor goez here -->
    <section class="card-body p-2">
      <textarea id="content" class="form-control" placeholder="Take a note..." v-model="note.content"></textarea>
    </section>
    <!-- footer -->
    <footer class="card-footer p-1">
      <!-- - category | tags -->
      <!-- - other opts buttons -->
      <button @click="done()" class="btn btn-primary btn-raised">Done</button>
      <button @click="cancel()" class="btn btn-primary btn-raised">Cancel</button>
    </footer>
  </section>
</template>

<script>
// TODO: we need to finetune this thing
import autoResize from 'autoresize-textarea';

export default {
  props: ['note'],
  mounted() {
    this._contentEditor = autoResize(this.$el.querySelector("#content"));
  },
  methods: {
    done() {
      // this._contentEditor.reset();
      this.$emit('doneEdit');
    },
    cancel() {
      // this._contentEditor.reset();
      this.$emit('cancelEdit');
    }
  }
}
</script>

<style>
</style>
