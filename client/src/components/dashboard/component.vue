<template>
  <section class="main container-flex">
    <div class="col-md-12">
      <header class="row">
        Ide jon majd a dashoard, ha kesz lesz
        &nbsp;
        <a
          href="#"
          @click="pullSnackbar"
        >Push snackbar</a>
      </header>
    </div>

  </section>
</template>

<script>
export default {

  methods: {
    pullSnackbar () {
      (new Promise((resolve, reject) => {
        setTimeout(resolve, 300);
      })).then(() => {
        throw new Error('Some test error message');
      }).catch((error) => {
        console.error('Error', error);
        this.$store.dispatch('UI/pushIOError', error);
      }).finally(() => { console.log('Finally!'); });
    }
  }
};
</script>

<style />
