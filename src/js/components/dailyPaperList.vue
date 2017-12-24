<template>
<div class="columns daily-paper-list" v-if="!isPapersEmpty">
  <div class="column is-2 daily-paper-meta">
    <h2 class="subtitle is-2 has-text-justified">{{ displayDate }}</h2>
  </div>
  <div class="column is-10">
    <paper-item
      v-for="paper in papers"
      :key="paper.id"
      :paper="paper"
      :subjects="subjects"
      :isSelected="selectedPaper && paper.id === selectedPaper.id"
      @selectItem="selectItem"
    ></paper-item>
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
    selectedPaper: Object,
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
  methods: {
    selectItem(paperId) {
      this.$emit('selectItem', paperId);
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

  .daily-paper-meta {
    padding: 1.5em 1em 0;
  }
}
</style>
