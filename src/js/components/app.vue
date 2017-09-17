<template>
  <div id="app">
    <div class="title">
      <h1>{{ message }}</h1>
    </div>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      message: 'Hello, Vue.js!',
    }
  },
}
</script>

<style lang="scss" scoped>
.title {
  h1 {
    font-size: 3em;
  }
}
</style>
