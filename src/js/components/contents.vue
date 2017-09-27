<template>
<div id="contents">
  <div class="columns is-gapless">
    <div class="column is-harf">
      <paper-list
        :subjects="subjects"
        :papers="papers"
        :selectedPaper="selectedPaper"
        :paperDetailHeight="paperDetailHeight"
        @selectItem="selectItem"
        @addPapers="addPapers"
      ></paper-list>
    </div>
    <div class="column is-harf">
      <paper-detail
        :paper="selectedPaper"
        :subject="selectedSubject"
        @updateHeight="updateHeight"
      ></paper-detail>
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
      selectedPaper: null,
      selectedSubject: null,
      paperDetailHeight: 0,
    }
  },
  methods: {
    selectItem(paperId) {
      for (let paper of this.papers) {
        if (paper.id === paperId) {
          this.selectedPaper = paper;
          this.selectedSubject = this.subjects[paper.rss_fetch_subject_id];
          break;
        }
      }
    },
    updateHeight(paperDetailHeight) {
      this.paperDetailHeight = paperDetailHeight;
    },
    addPapers(papers) {
      this.$set(this, 'papers', this.papers.concat(papers));
    },
  },
};
</script>

<style lang="scss" scoped>
</style>
