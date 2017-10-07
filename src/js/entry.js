import Vue from 'vue';
import app from './components/app.vue';
import registerFilters from './utils/filters.js';

registerFilters(Vue);

new Vue({
  el: '#app',
  components: {
    app,
  },
});
