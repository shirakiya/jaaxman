<template>
<section id="contents" class="columns">
  <div class="column is-10 is-offset-1">
    <subject-tab
      :subjects="subjects"
      :selectedSubject="(selectedSubject) ? selectedSubject.name : ''"
      @selectSubject="selectSubject"
    ></subject-tab>
    <paper-list
      :subjects="subjects"
      :papers="papers"
      :selectedSubject="selectedSubject"
      @addPapers="addPapers"
    ></paper-list>
  </div>
</section>
</template>

<script>
import subjectTab from './subjectTab.vue';
import paperList from './paperList.vue';

export default {
  components: {
    subjectTab,
    paperList,
  },
  data() {
    return {
      subjects: window.subjects,
      papers: window.papers,
      selectedSubject: null,
    };
  },
  methods: {
    selectSubject(subjectName) {
      if (subjectName) {
        for (let subject of this.subjects) {
          if (subject.name === subjectName) {
            this.selectedSubject = subject;
            break;
          }
        }
      } else {
        this.selectedSubject = null;
      }
    },
    addPapers(papers) {
      this.$set(this, 'papers', this.papers.concat(papers));
    },
  },
};
</script>

<style lang="scss" scoped>
#contents {
  padding-top: 1em;
}
</style>
