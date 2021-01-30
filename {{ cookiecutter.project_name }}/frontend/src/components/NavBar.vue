<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-brand href="#">
        {{cookiecutter.project_name}}
        <!-- <img class="logo" alt="{{cookiecutter.project_name}} logo" src="../assets/logo.png" /> -->
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/">/</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item to="/about">About</b-nav-item>
          <b-navbar-nav v-if="! getId">
            
            <b-nav-item to="/login">Connexion</b-nav-item>
            <b-nav-item to="/register">Inscription</b-nav-item>
          </b-navbar-nav>
          <b-navbar-nav v-else>
            <b-nav-item to="/profile">
              <font-awesome-icon icon="user" />
              {% raw %}{{ getId }}{% endraw %}
            </b-nav-item>
            <b-nav-item to="#" v-if="getId" v-on:click="logout()" href="#">
              logout
            </b-nav-item>
            
            <b-nav-item-dropdown right>
              <!-- Using 'button-content' slot -->
              <template v-slot:button-content>
                <em>User</em>
              </template>
              <b-dropdown-item href="#">Profil</b-dropdown-item>
              <b-dropdown-item href="#">
                <b-nav-item to="#" v-if="getId" v-on:click="logout()" href="#">
                  Déconnexion
                </b-nav-item>
              </b-dropdown-item>
            </b-nav-item-dropdown>
            <b-avatar text=""></b-avatar>
          </b-navbar-nav>

        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { mapGetters } from 'vuex'

@Component({
  computed: mapGetters(['getId'])
})
export default class NavBar extends Vue {
  
}
</script>

<style>
img.logo {
  max-height: 30px;
  margin-left: -10px;
}
</style>
