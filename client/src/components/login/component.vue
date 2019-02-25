<template>
  <section class="container-flex">
    <!-- <div class="row"> -->
    <div class="col-md-12">
      <div
        class="row justify-content-center align-items-center"
        style="height:100vh"
      >
        <div class="col-4">
          <div class="card">
            <div class="card-body">
              <form
                action=""
                autocomplete="off"
              >
                <div class="form-group">
                  <input
                    autofocus
                    autocomplete="off"
                    type="text"
                    class="form-control"
                    ref="username"
                    placeholder="Username"
                    v-model="username"
                  >
                </div>
                <div class="form-group">
                  <input
                    autocomplete="off"
                    type="password"
                    class="form-control"
                    ref="password"
                    placeholder="Password"
                    v-model="password"
                    @keyup.enter="login"
                  >
                </div>
                <button
                  type="button"
                  id="sendlogin"
                  class="btn btn-primary"
                  @click="login"
                >Login</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login () {
      this.$store.dispatch('User/login', { username: this.username, password: this.password });
      // reset for if login was not successful
      this.username = '';
      this.password = '';
      this.$refs.username.focus();
    }
  }
};
</script>

<style>
</style>
