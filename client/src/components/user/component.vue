<template>
  <section class="main container-flex">
    <div class="row">
      <div class="col-md-6 col-sm-12">

        <section class="card bg-light mx-1 my-2">
          <div class="card-body py-2">
            Some basic profile stuff will go here
          </div>
        </section>

      </div>
      <div class="col-md-6 col-sm-12">

        <section class="card bg-light mx-1 my-2">
          <div class="card-body py-2">
            <ul class="connect">
              <li>
                <!-- GOOGLE INTEGRATION SETTINGS -->
                <h5>Google integration </h5>
                <ul v-if="google.connected">
                  <li>
                    <input
                      type="checkbox"
                      v-model="google.enableGMail"
                      id="syncGMail"
                    />
                    <label for="syncGMail">Sync Google mail</label>
                  </li>
                  <li>
                    <input
                      type="checkbox"
                      v-model="google.enableGTasks"
                      id="syncGTasks"
                    />
                    <label for="syncGTasks">Sync Google tasks</label>
                  </li>
                  <li>
                    <input
                      type="checkbox"
                      v-model="google.enableGCalendar"
                      id="syncGCalender"
                    />
                    <label for="syncGCalender">Sync Google calendar</label>
                  </li>
                </ul>
                <template v-if="google.connected">
                  <button
                    class="btn btn-danger"
                    @click="signOutGoogle"
                  >Disconnect Google Account</button>
                </template>
                <template else>
                  <button
                    class="btn btn-success"
                    @click="signInGoogle"
                  >Connect Google Account</button>
                </template>
                <!-- / GOOGLE INTEGRATION SETTINGS -->
              </li>
              <li>
                <h5>Connect habitica</h5>
              </li>
              <li>
                <h5>Connect github </h5>
              </li>
            </ul>

          </div>
        </section>

      </div>
    </div>
  </section>

</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from 'vuex';

export default {
  data () {
    return {
    };
  },
  computed: {
    ...mapState('User/SyncGoogle', { google: 'settings' })
  },
  methods: {
    signInGoogle () {
      this.$gAuth.getAuthCode()
        .then(authCode => {
          // on success
          console.log('authCode', authCode);
          return this.$http.post('http://your-backend-server.com/auth/google', { code: authCode, redirect_uri: 'postmessage' });
        })
        .then(response => {
          // after ajax
        })
        .catch(error => {
          // on fail do something
          console.log('Error', error);
        });
    },
    signOutGoogle () {
      // you can use promise from v1.1.0 also
      this.$gAuth.signOut()
        .then(() => {
          // things to do when sign-out succeeds
        })
        .catch(error => {
          // things to do when sign-out fails
          console.log('Error', error);
        });
    }
  }
};
</script>

<style lang="scss" scoped>
section {
  &.main {
    .row {
      margin: 0 !important;
    }
    .connect {
      list-style-type: none;
      li {
        margin-bottom: 18px;
      }
      ul {
        list-style-type: none;
      }
    }
  }
}
</style>
