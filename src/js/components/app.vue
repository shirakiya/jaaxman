<template>
  <div id="app">
    <div class="title">
      <h1>{{ message }}</h1>
    </div>
    <icon name="flag"></icon>
  </div>
</template>

<script>
import Icon from 'vue-awesome/components/Icon.vue';
import 'vue-awesome/icons/flag';

export default {
  components: {
    Icon,
  },
  data: () => {
    return {
      message: 'Hello, Vue.js!',
    }
  },
};
</script>

<style lang="scss" scoped>
</style>
