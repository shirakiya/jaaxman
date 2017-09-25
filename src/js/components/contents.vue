<template>
<div id="contents">
  <div class="columns is-gapless">
    <div class="column is-harf">
      <paper-list :subjects="subjects" :papers="papers"></paper-list>
    </div>
    <div class="column is-harf">
      <paper-detail></paper-detail>
    </div>
  </div>
</div>
</template>

<script>
import paperList from './paperList.vue';
import paperDetail from './paperDetail.vue';

export default {
  components: {
    paperList,
    paperDetail,
  },
  data() {
    return {
      subjects: window.subjects,
      papers: window.papers,
    }
  },
};
</script>

<style lang="scss" scoped>
</style>
