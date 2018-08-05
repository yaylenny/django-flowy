import Vue from 'vue';
import App from './views/App.vue';

/* * *    SETUP VUE APPLICATION   * * */
const elementID="application";
const config={
  el: `#${elementID}`,
  render:h=>h( App )
};


/* * *    VUEX - STORE    * * */
import Vuex from "vuex";
import storeConfig from './store/store.js';
Vue.use( Vuex );
config.store=new Vuex.Store( storeConfig );



/* * *      INSTANTIATE THE COMPONENT    * * */
new Vue( config );
