<template>
<nav class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <img :src="brandImage" alt="Jaaxman"></img>
    </a>
    <div class="navbar-burger burger" :class="{ 'is-active': isShownMenu }" v-on:click="toggleMenu">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
  <div class="navbar-menu" :class="{ 'is-active': isShownMenu }">
    <div class="navbar-end">
      <a class="navbar-item" href="/" target="_brank">
        About
      </a>
    </div>
  </div>
</nav>
</template>

<script>
import { getImgPath } from '../utils/statics.js';

export default {
  data() {
    return {
      isShownMenu: false,
    }
  },
  computed: {
    brandImage() {
      return getImgPath('logo_inline_512.png');
    },
  },
  methods: {
    toggleMenu() {
      this.isShownMenu = this.isShownMenu ? false : true;
    },
  }
};
</script>

<style lang="scss" scoped>
.navbar {
  border-bottom: 1px solid lightgray;
  box-shadow: 0 1px 3px rgba(10, 10, 10, 0.1);

  .navbar-main {
    font-size: 24px;
    font-weight: bold;
  }
}
</style>
