<template>
  <div class="form-group">
    <input class="form-control" type="text" autofocus autocomplete="off" placeholder="Title" v-model="note.title" />
    <!-- text editor goez here -->
    <textarea id="content" class="form-control" placeholder="Take a note..." v-model="note.content"></textarea>
    <!-- footer -->
    <!-- - category | tags -->
    <!-- - other opts buttons -->
    <button @click="done()" class="btn btn-primary btn-raised">Done</button>
    <button @click="cancel()" class="btn btn-primary btn-raised">Cancel</button>
  </div>
</template>

<script>
export default {
  props: ['note'],
  methods: {
    done() {
      this.$emit('doneEdit');
    },
    cancel() {
      this.$emit('cancelEdit');
    }
  }
}
</script>

<style>
</style>
