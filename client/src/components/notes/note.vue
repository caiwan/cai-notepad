<template>
  <section class="card bg-light mx-1 my-2">
    <header class="card-header p-2">{{ note.title }}
      <button @click="edit()">Edit</button>
      <button @click="remove()">Delete</button>
      <button @click="pin()">Pin</button>
    </header>
    <section class="card-body p-2">
      <vue-markdown :source="note.content"></vue-markdown>
    </section>
    <footer class="card-footer p-2">
      Cagegory | tags <br />
    </footer>
  </section>
</template>

<script>
export default {
  props: ['note'],
  computed: {
  },
  methods: {
    edit() {
      this.$emit('editNote');
    },
    remove(note) {
      this.$emit('removeNote');
    },
    pin(note) {
      this.$emit('pinNote');
    }
  }
}
</script>

<style lang="scss">
</style>
