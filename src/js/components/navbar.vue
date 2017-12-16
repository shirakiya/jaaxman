<template>
<nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
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
    <div class="navbar-start">
    </div>
    <div class="navbar-end">
      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          Info
        </a>
        <div class="navbar-dropdown">
          <a class="navbar-item" href="/" target="_brank">
            Jaaxmanについて
          </a>
          <a class="navbar-item" @click="openTermModal" @close="closeTermModal">
            利用規約
          </a>
        </div>
      </div>
      <div class="navbar-item">
          <google-attribution-regular></google-attribution-regular>
      </div>
    </div>
  </div>
  <termModal :isActive="isActiveTerm" @close="closeTermModal"></termModal>
</nav>
</template>

<script>
import googleAttributionRegular from './googleAttributionRegular.vue';
import termModal from './termModal.vue';
import { getImgPath } from '../utils/statics.js';

export default {
  components: {
    googleAttributionRegular,
    termModal,
  },
  data() {
    return {
      isShownMenu: false,
      isActiveTerm: false,
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
    openTermModal() {
      this.isActiveTerm = true;
    },
    closeTermModal() {
      this.isActiveTerm = false;
    },
  }
};
</script>

<style lang="scss" scoped>
.navbar {
  border-bottom: 1px solid lightgray;
  box-shadow: 0 1px 3px rgba(10, 10, 10, 0.1);
  z-index: 20;

  .navbar-menu {
    font-size: 1rem;
  }
}
</style>
