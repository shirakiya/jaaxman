<template>
<span class="google-attribution-regular">
  <a href="http://translate.google.com/?hl=ja" target="_blank">
    <img :src="googleLogo" :style="imgStyle" alt="google-attribution-greyscale-regular"></img>
  </a>
</span>
</template>

<script>
import { getImgPath } from '../utils/statics.js';

export default {
  props: {
    width: {
      type: Number,
      default: 200,
    }
  },
  computed: {
    googleLogo() {
      return getImgPath('greyscale-regular@2x.png');
    },
    imgStyle() {
      return {
        width: this.width + 'px',
        verticalAlign: 'text-bottom',
      };
    },
  },
};
</script>

<style lang="scss" scoped>
</style>
