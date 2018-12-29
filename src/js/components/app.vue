<template>
<div>
  <navbar></navbar>
  <contents></contents>
  <brand-footer></brand-footer>
</div>
</template>

<script>
import navbar from './navbar.vue';
import contents from './contents.vue';
import brandFooter from './brandFooter.vue';

export default {
  components: {
    navbar,
    contents,
    brandFooter,
  },
};
</script>
