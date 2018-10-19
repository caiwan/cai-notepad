<template>
  <div>
    <header>{{ note.title }}
      <button @click="edit()">Edit</button>
      <button @click="remove()">Delete</button>
      <button @click="pin()">Pin</button>
    </header>
    {{note.content}}
    <footer>
      Cagegory | tags <br />
      <hr />
    </footer>
  </div>
</template>

<script>
export default {
  props: ['note'],
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
