import Vue from 'vue';
import registerFilters from './utils/filters.js';
import app from './components/app.vue';
import flatPickr from 'vue-flatpickr-component';

Vue.use(flatPickr);
registerFilters(Vue);

new Vue({
  el: '#app',
  components: {
    app,
  },
});
