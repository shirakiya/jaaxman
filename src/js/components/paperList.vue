<template>
<div id="paper-list">
  <div class="paper-list-container">
    <div id="paper-list-content">
      <daily-paper-list
        v-for="(filteredPaperValues, date) in filteredPapers"
        :key="date"
        :date="date"
        :papers="filteredPaperValues"
        :subjects="subjects"
      ></daily-paper-list>
      <div class="paper-item-end" v-if="showLoader">
        <a class="button is-loading"></a>
      </div>
    </div>
  </div>
  <paper-modal
    v-if="selectedPaper"
    :paper="selectedPaper"
    :subject="subjectOfSelectedPaper"
    :isActive="isActivePaperModal"
  ></paper-modal>
</div>
</template>

<script>
import axios from 'axios';
import dailyPaperList from './dailyPaperList.vue';
import paperModal from './paperModal.vue';

export default {
  props: {
    subjects: Array,
    papers: Object,
    selectedPaperId: {
      type: Number,
      required: false,
    },
    selectedSubmitType: {
      type: Object,
      required: false,
    },
    selectedSubject: {
      type: Object,
      required: false,
    },
    stopAutoLoading: Boolean,
  },
  components: {
    dailyPaperList,
    paperModal,
  },
  mounted() {
    window.addEventListener('scroll', this.checkAndFetchPapers);
    if (this.selectedPaperId) {
      this.selectOrFetchPaper(this.selectedPaperId);
    }
  },
  beforeDestory() {
    window.removeEventListener('scroll', this.checkAndFetchPapers);
  },
  data() {
    return {
      inRequest: false,
      isFetchCompleted: false,
      selectedPaper: null,
    };
  },
  watch: {
    selectedPaperId() {
      this.selectOrFetchPaper(this.selectedPaperId);
    },
    selectedSubject() {
      setTimeout(() => {
        this.checkAndFetchPapers();
      }, 500);
    },
    selectedSubmitType() {
      setTimeout(() => {
        this.checkAndFetchPapers();
      }, 500);
    },
  },
  computed: {
    filteredPapers() {
      let papers = this.papers;
      papers = this.filteredPapersBySubject(papers);
      papers = this.filteredPapersBySubmitType(papers);
      return papers;
    },
    isActivePaperModal() {
      return this.selectedPaper != null;
    },
    subjectOfSelectedPaper() {
      if (!this.selectedPaper) {
        return null;
      }
      for (let subject of this.subjects) {
        if (subject.id == this.selectedPaper.rss_fetch_subject_id) {
          return subject;
        }
      }
    },
    showLoader() {
      return !this.isFetchCompleted && !this.stopAutoLoading;
    },
  },
  methods: {
    filteredPapersBySubject(papers) {
      if (!this.selectedSubject) {
        return papers;
      } else {
        let filteredPapers = {};
        Object.keys(papers).map((key) => {
          filteredPapers[key] = papers[key].filter((paper) => {
            return paper.rss_fetch_subject_id === this.selectedSubject.id;
          });
        });
        return filteredPapers;
      }
    },
    filteredPapersBySubmitType(papers) {
      if (!this.selectedSubmitType) {
        return papers;
      } else {
        let filteredPapers = {};
        Object.keys(papers).map((key) => {
          filteredPapers[key] = papers[key].filter((paper) => {
            return paper.submit_type === this.selectedSubmitType.name;
          });
        });
        return filteredPapers;
      }
    },
    fetchPaper(paperId) {
      return axios.get(`/api/paper/${paperId}`);
    },
    fetchPapers() {
      return axios.get('/api/papers', {
        params: {
          count: this.getPaperLength(this.papers),
        },
      });
    },
    selectPaper(paperId) {
      for (let key of Object.keys(this.papers)) {
        for (let paper of this.papers[key]) {
          if (paper.id === paperId) {
            return paper;
          }
        }
      }
    },
    selectOrFetchPaper(paperId) {
      if (!paperId) {
        this.selectedPaper = null;
      } else {
        let selectedPaper = this.selectPaper(paperId);
        if (selectedPaper) {
          this.selectedPaper = selectedPaper;
        } else {
          this.fetchPaper(paperId).then(res => {
            this.selectedPaper = res.data;
          }).catch(error => {
            if (error.response.status === 404) {
              this.$router.replace({ name: 'home' });
            } else {
              console.error(error);
            }
          });
        }
      }
    },
    getScrollBottom() {
      const body = document.body;
      const html = document.documentElement;
      const scrollTop = body.scrollTop || html.scrollTop;
      return html.scrollHeight - html.clientHeight - scrollTop;
    },
    getPaperLength(papers) {
      let count = 0;
      Object.keys(papers).map((key) => {
        count += papers[key].length;
      });
      return count;
    },
    checkAndFetchPapers() {
      const scrollBottom = this.getScrollBottom();
      if (this.stopAutoLoading || this.isFetchCompleted || this.inRequest || scrollBottom >= 300) {
        return;
      }
      this.inRequest = true;
      this.fetchPapers().then(res => {
        this.inRequest = false;
        const papers = res.data.papers;
        if (this.getPaperLength(papers) === 0) {
          this.isFetchCompleted = true;
        } else {
          this.$emit('addPapers', papers);
        }
      }).catch(error => {
        this.inRequest = false;
        console.error(error);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
#paper-list {

  .paper-list-container {
    margin: 0 1em 0;
    height: 100%;

    .paper-item-end {
      text-align: center;
      height: 30px;

      .button {
        &.is-loading {
          font-size: 24px;
          border: none;
        }
      }
    }
  }
}
</style>
