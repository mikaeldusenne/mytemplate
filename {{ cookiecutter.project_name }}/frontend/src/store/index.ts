import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        id: null,
    },
    mutations: {
      	changeid(state, id){
			state.id = id;
		}
    },
    actions: {
		setId({commit}, id){
			commit("changeid", id)
		}
    },
    modules: {
        
    },
    getters: {
        getId: state => state.id
    },
});
