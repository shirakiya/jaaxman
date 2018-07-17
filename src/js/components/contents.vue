<template>
<section id="contents" class="columns">
  <div class="column is-10 is-offset-1">
    <filtering-card
      :subjects="subjects"
      :submitTypes="submitTypes"
      :defaultSubmitType="selectedSubmitType"
      :defaultSubject="selectedSubject"
      :defaultDate="selectedDate"
      :defaultSearchQuery="searchQuery"
      :minDate="minDate"
      :maxDate="maxDate"
    ></filtering-card>
    <paper-list
      v-if="!isPapersEmpty"
      :subjects="subjects"
      :papers="papers"
      :selectedPaperId="selectedPaperId"
      :selectedSubmitType="selectedSubmitType"
      :selectedSubject="selectedSubject"
      :stopAutoLoading="isReplaced"
      @addPapers="addPapers"
    ></paper-list>
    <div class="paper-loading has-text-centered" v-else-if="isLoadingPaper">
      <a class="button is-loading"></a>
    </div>
    <article class="message is-warning" v-else>
      <div class="message-body">
        論文が存在しません。
      </div>
    </article>
  </div>
</section>
</template>

<script>
import axios from 'axios';
import filteringCard from './filteringCard.vue';
import paperList from './paperList.vue';

export default {
  props: {
    selectedSubmitTypeName: {
      type: String,
      default: null,
    },
    selectedSubjectName: {
      type: String,
      default: null,
    },
    selectedDate: {
      type: String,
      default: null,
    },
    searchQuery: {
      type: String,
      default: null,
    },
    selectedPaperId: {
      type: Number,
      default: null,
    },
  },
  components: {
    filteringCard,
    paperList,
  },
  data() {
    return {
      subjects: window.subjects,
      submitTypes: window.submitTypes,
      isLoadingPaper: true,
      papers: {},
      allPapers: {},
      minDate: '2017-12',
    };
  },
  watch: {
    selectedDate() {
      // 条件が一つでもあるならば新たに検索を行う
      if (this.selectedDate || this.searchQuery) {
        this.fetchPapersWithCondition(this.selectedDate, this.searchQuery).then(res => {
          this.$set(this, 'papers', res.data.papers);
        });
      } else {
        this.$set(this, 'papers', this.allPapers);
      }
    },
    searchQuery() {
      // 条件が一つでもあるならば新たに検索を行う
      if (this.selectedDate || this.searchQuery) {
        this.fetchPapersWithCondition(this.selectedDate, this.searchQuery).then(res => {
          this.$set(this, 'papers', res.data.papers);
        });
      } else {
        this.$set(this, 'papers', this.allPapers);
      }
    },
  },
  created() {
    this.fetchPapers();
  },
  computed: {
    maxDate() {
      const dates = Object.keys(this.allPapers);
      return (dates.length !== 0) ? dates[0] : '2017-12';
    },
    isReplaced() {
      return Boolean(this.selectedDate) || Boolean(this.searchQuery);
    },
    isPapersEmpty() {
      return Object.keys(this.papers).length === 0;
    },
    selectedSubmitType() {
      if (!this.selectedSubmitTypeName) {
        return null;
      }
      else if (this.selectedSubmitTypeName === '全て') {
        return null;
      }
      else {
        for (let submitType of this.submitTypes) {
          if (submitType.display_name === this.selectedSubmitTypeName) {
            return submitType;
          }
        }
      }
    },
    selectedSubject() {
      if (!this.selectedSubjectName) {
        return null;
      }
      else if (this.selectedSubjectName === '全て') {
        return null;
      }
      else {
        for (let subject of this.subjects) {
          if (subject.name === this.selectedSubjectName) {
            return subject;
          }
        }
      }
    },
  },
  methods: {
    fetchPapersWithCondition(date, query) {
      return axios.get('/api/papers', {
        params: {
          date: date,
          query: query,
        },
      });
    },
    fetchPapersAsDefault() {
      return axios.get('/api/papers', {
        params: {
          count: 0,
        },
      });
    },
    fetchPapers() {
      if (this.selectedDate || this.searchQuery) {
        this.fetchPapersWithCondition(this.selectedDate, this.searchQuery).then(res => {
          this.isLoadingPaper = false;
          this.$set(this, 'papers', res.data.papers);
          return this.fetchPapersAsDefault();
        }).then(res => {
          this.$set(this, 'allPapers', res.data.papers);
        }).catch(error => {
          console.error(error);
        });
      } else {
        this.fetchPapersAsDefault().then(res => {
          this.isLoadingPaper = false;
          this.$set(this, 'papers', res.data.papers);
          this.$set(this, 'allPapers', res.data.papers);
        }).catch(error => {
          console.error(error);
        });
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
      this.$set(this, 'allPapers', assignedPapers);
    },
  },
};
</script>

<style lang="scss" scoped>
#contents {
  padding-top: 1em;

  .paper-loading {
    .button {
      &.is-loading {
        font-size: 36px;
        border: none;
      }
    }
  }
}
</style>
