<template>
<span class="google-attribution-short">
  <a href="http://translate.google.com/?hl=ja" target="_blank">
    <img :src="googleLogo" :style="imgStyle" alt="google-attribution-greyscale-short"></img>
  </a>
</span>
</template>

<script>
import { getImgPath } from '../utils/statics.js';

export default {
  props: {
    width: {
      type: Number,
      default: 100,
    }
  },
  computed: {
    googleLogo() {
      return getImgPath('greyscale-short@2x.png');
    },
    imgStyle() {
      return {
        width: this.width + 'px',
      };
    },
  },
};
</script>
