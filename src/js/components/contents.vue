<template>
<section id="contents" class="columns">
  <div class="column is-10 is-offset-1">
    <filtering-card
      :subjects="subjects"
      :submitTypes="submitTypes"
      @selectSubject="selectSubject"
      @selectSubmitType="selectSubmitType"
      @replacePapers="replacePapers"
      @undoPapers="undoPapers"
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
      allPapers: null,
      selectedSubject: null,
      selectedSubmitType: null,
    };
  },
  computed: {
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
      this.$set(this, 'allPapers', this.papers)
      this.$set(this, 'papers', papers);
    },
    undoPapers() {
      if (this.allPapers) {
        this.$set(this, 'papers', this.allPapers);
        this.$set(this, 'allPapers', null);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#contents {
  padding-top: 1em;
}
</style>
