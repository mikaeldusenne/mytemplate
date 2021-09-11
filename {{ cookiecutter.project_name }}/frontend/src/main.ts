import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faEdit } from "@fortawesome/free-solid-svg-icons";
import { faMinusSquare } from "@fortawesome/free-solid-svg-icons";
import { faPlusSquare } from "@fortawesome/free-solid-svg-icons";

import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";


Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

library.add(faEdit);
library.add(faMinusSquare);
library.add(faPlusSquare);

Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.component("v-select", vSelect);


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
