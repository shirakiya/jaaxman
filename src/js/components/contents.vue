<template>
<section id="contents" class="columns">
  <div class="column is-10 is-offset-1">
    <filtering-card
      :subjects="subjects"
      :submitTypes="submitTypes"
      @selectSubject="selectSubject"
      @selectSubmitType="selectSubmitType"
    ></filtering-card>
    <paper-list
      :subjects="subjects"
      :papers="papers"
      :selectedSubject="selectedSubject"
      :selectedSubmitType="selectedSubmitType"
      @addPapers="addPapers"
    ></paper-list>
  </div>
</section>
</template>

<script>
import filteringCard from './filteringCard.vue';
import paperList from './paperList.vue';

export default {
  components: {
    filteringCard,
    paperList,
  },
  data() {
    return {
      subjects: window.subjects,
      papers: window.date_to_papers,
      submitTypes: window.submitTypes,
      selectedSubject: null,
      selectedSubmitType: null,
    };
  },
  methods: {
    selectSubject(subjectName) {
      if (subjectName === 'ALL') {
        this.selectedSubject = null;
      } else {
        for (let subject of this.subjects) {
          if (subject.name === subjectName) {
            this.selectedSubject = subject;
            break;
          }
        }
      }
    },
    selectSubmitType(selectedSubmitType) {
      if (selectedSubmitType === 'ALL') {
        this.selectedSubmitType = null;
      } else {
        for (let submitType of this.submitTypes) {
          if (submitType.display_name === selectedSubmitType) {
            this.selectedSubmitType = submitType;
            break;
          }
        }
      }
    },
    addPapers(papers) {
      const assignedPapers = Object.assign({}, this.papers);
      Object.keys(papers).map((key) => {
        if (key in assignedPapers) {
          assignedPapers[key] = assignedPapers[key].concat(papers[key]);
        } else {
          assignedPapers[key] = papers[key];
        }
      });
      this.$set(this, 'papers', assignedPapers);
    },
  },
};
</script>

<style lang="scss" scoped>
#contents {
  padding-top: 1em;
}
</style>
