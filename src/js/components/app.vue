<template>
<div>
  <navbar></navbar>
  <contents></contents>
</div>
</template>

<script>
import navbar from './navbar.vue';
import contents from './contents.vue';

export default {
  components: {
    navbar,
    contents,
  },
};
</script>

<style lang="scss" scoped>
</style>
