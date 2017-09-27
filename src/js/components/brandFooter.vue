<template>
<footer>
  <div class="footer-content">
    <span><a href="/">Jaaxman</a> created by <a href="https://twitter.com/shirakiya831">shirakiya</a>.</span>
    <google-attribution-regular></google-attribution-regular>
    <span @click="openTermModal"><a>利用規約</a></span>
  </div>
  <term-modal :isActive="isActiveTerm" @close="closeTermModal"></term-modal>
</footer>
</template>

<script>
import googleAttributionRegular from './googleAttributionRegular.vue';
import termModal from './termModal.vue';

export default {
  components: {
    googleAttributionRegular,
    termModal,
  },
  data() {
    return {
      isActiveTerm: false,
    };
  },
  methods: {
    openTermModal() {
      console.log('hoge');
      this.isActiveTerm = true;
    },
    closeTermModal() {
      this.isActiveTerm = false;
    },
  },
};
</script>

<style lang="scss" scoped>
footer {
  border-top: 2px solid lightgrey;
  padding: 1em 2em;

  .footer-content {
    text-align: center;
  }

  span {
    margin-right: .5em;
  }
}
</style>
