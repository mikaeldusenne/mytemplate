<template>
  <div class="container-fluid">
    <h1>{{cookiecutter.project_name}}</h1>
  </div>
</template>


<script>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { NumType, CategoricalOptions, CategoricalValue, Variable } from "@/types";
import axios from 'axios'

axios.defaults.baseURL = '{{ cookiecutter.root_url }}';

@Component
export default class Home extends Vue {

  
}
</script>

<style>
body{
  background: #f9f9f9;
}
.nav-tabs .nav-link.active{
  background: #f9f9f9;
}
</style>
