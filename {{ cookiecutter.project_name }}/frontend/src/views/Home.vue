<template>
  <div class="container-fluid">
    {% raw %}{{ message }}{% endraw %}
  </div>
</template>


<script>
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { NumType, CategoricalOptions, CategoricalValue, Variable } from "@/types";
import { required, between, integer } from "vuelidate/lib/validators";
import axios from 'axios'

axios.defaults.baseURL = '{{ cookiecutter.root_url }}';

@Component
export default class Home extends Vue {

  message = "Welcome Home"
  
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
