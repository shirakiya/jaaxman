import Vue from 'vue';
import VueRouter from 'vue-router';
import flatPickr from 'vue-flatpickr-component';
import registerFilters from './utils/filters.js';
import contents from './components/contents.vue';
import navbar from './components/navbar.vue';
import brandFooter from './components/brandFooter.vue';

Vue.use(VueRouter);
Vue.use(flatPickr);
registerFilters(Vue);

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      components: {
        default: contents,
        navbar: navbar,
        brandFooter: brandFooter,
      },
      props: {
        default: (route) => ({
          selectedSubmitTypeName: route.query.submitType || null,
          selectedSubjectName: route.query.subject || null,
          selectedDate: route.query.date || null,
          searchQuery: route.query.query || null,
          selectedPaperId: Number(route.query.paperId) || null,
        }),
        navbar: false,
        brandFooter: false,
      },
    },
  ],
});

new Vue({
  el: '#app',
  router,
});
