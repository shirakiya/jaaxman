<template>
<section id="contents" class="columns">
  <div class="column is-10 is-offset-1">
    <filtering-card
      :subjects="subjects"
      :submitTypes="submitTypes"
      :minDate="minDate"
      :maxDate="maxDate"
      @selectSubject="selectSubject"
      @selectSubmitType="selectSubmitType"
      @replacePapers="replacePapers"
      @resetOriginalPapers="resetOriginalPapers"
    ></filtering-card>
    <paper-list
      v-if="!isPapersEmpty"
      :subjects="subjects"
      :papers="papers"
      :selectedSubject="selectedSubject"
      :selectedSubmitType="selectedSubmitType"
      :stopAutoLoading="isReplaced"
      @addPapers="addPapers"
    ></paper-list>
    <article class="message is-warning" v-else>
      <div class="message-body">
        論文が存在しません。
      </div>
    </article>
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
      allPapers: window.date_to_papers,
      minDate: '2017-12',
      selectedSubject: null,
      selectedSubmitType: null,
    };
  },
  computed: {
    maxDate() {
      const dates = Object.keys(window.date_to_papers);
      return (dates.length !== 0) ? dates[0] : '2017-12';
    },
    isReplaced() {
      return this.allPapers !== null;
    },
    isPapersEmpty() {
      return Object.keys(this.papers).length === 0;
    },
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
    replacePapers(papers) {
      this.$set(this, 'papers', papers);
    },
    resetOriginalPapers() {
      this.$set(this, 'papers', this.allPapers);
    },
  },
};
</script>

<style lang="scss" scoped>
#contents {
  padding-top: 1em;
}
</style>
