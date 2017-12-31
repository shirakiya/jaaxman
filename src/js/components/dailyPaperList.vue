<template>
<div class="daily-paper-list" v-if="!isPapersEmpty">
  <div class="daily-paper-title">
    <h2 class="subtitle is-2 has-text-justified">{{ displayDate }}</h2>
  </div>
  <div class="columns">
    <div class="column is-2">
    </div>
    <div class="column is-10">
      <paper-item
        v-for="paper in papers"
        :key="paper.id"
        :paper="paper"
        :subjects="subjects"
      ></paper-item>
    </div>
  </div>
</div>
</template>

<script>
import moment from 'moment';
import paperItem from './paperItem.vue';

export default {
  props: {
    date: String,
    papers: Array,
    subjects: Array,
  },
  components: {
    paperItem,
  },
  data() {
    return {
    };
  },
  computed: {
    displayDate() {
      return moment(this.date).format('M/D');
    },
    isPapersEmpty() {
      return this.papers.length < 1;
    },
  },
};
</script>

<style lang="scss" scoped>
.daily-paper-list {
  margin-top: 1em;

  &:first-child {
    margin-top: 0;
  }

  .daily-paper-title {
    background-color: whitesmoke;
    margin-bottom: .5em;
    padding: .5em 1.5em;
  }
}
</style>
