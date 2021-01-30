import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

// import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faEdit } from "@fortawesome/free-solid-svg-icons";
import { faMinusSquare } from "@fortawesome/free-solid-svg-icons";
import { faPlusSquare } from "@fortawesome/free-solid-svg-icons";

import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

import Vuelidate from "vuelidate";

Vue.use(BootstrapVue);
// Vue.use(BootstrapVueIcons);
Vue.use(IconsPlugin);

library.add(faEdit);
library.add(faMinusSquare);
library.add(faPlusSquare);

Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.component("v-select", vSelect);

Vue.use(Vuelidate);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
