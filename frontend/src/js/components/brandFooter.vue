<template>
<footer>
  <div class="footer-content">
    <span><a href="/">Jaaxman</a> created by <a href="https://twitter.com/shirakiya831" target="_blank">shirakiya</a>.</span>
    <google-attribution-regular></google-attribution-regular>
  </div>
</footer>
</template>

<script>
import googleAttributionRegular from './googleAttributionRegular.vue';

export default {
  components: {
    googleAttributionRegular,
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
