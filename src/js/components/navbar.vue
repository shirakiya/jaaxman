<template>
<nav id="navbar" class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="/">Jaaxman</a>
    <div class="navbar-burger burger" :class="{ 'is-active': isShownMenu }" v-on:click="toggleMenu">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
  <div id="navbar-menu" class="navbar-menu" :class="{ 'is-active': isShownMenu }">
    <div class="navbar-end">
      <a class="navbar-item" href="/" target="_brank">
        About
      </a>
    </div>
  </div>
</nav>
</template>

<script>
export default {
  data() {
    return {
      isShownMenu: false,
    }
  },
  methods: {
    toggleMenu() {
      this.isShownMenu = this.isShownMenu ? false : true;
    },
  }
};
</script>

<style lang="scss" scoped>
#navbar {
  border-bottom: 1px solid lightgray;
}
</style>
