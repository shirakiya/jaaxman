<template>
<div id="paper-list">
  <div class="paper-list-container">
    <div id="paper-list-content">
      <paper-item
        v-for="paper in filteredPapers"
        :key="paper.id"
        :paper="paper"
        :subjects="subjects"
        :isSelected="selectedPaper && paper.id === selectedPaper.id"
        @selectItem="selectItem"
      ></paper-item>
      <div class="paper-item-end" v-if="!isFetchCompleted">
        <a class="button is-loading"></a>
      </div>
    </div>
  </div>
  <paper-modal
    :paper="selectedPaper"
    :subject="subjectOfSelectedPaper"
    :isActive="isActivePaperModal"
    @closePaperModal="closePaperModal"
    v-if="selectedPaper"
  ></paper-modal>
</div>
</template>

<script>
import paperItem from './paperItem.vue';
import paperModal from './paperModal.vue';
import axios from 'axios';

export default {
  props: {
    subjects: Array,
    papers: Array,
    selectedSubject: {
      type: Object,
      required: false,
    },
  },
  components: {
    paperItem,
    paperModal,
  },
  mounted() {
    window.addEventListener('scroll', this.checkAndFetchPapers);
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
  computed: {
    filteredPapers() {
      if (!this.selectedSubject) {
        return this.papers;
      }
      else {
        return this.papers.filter((paper) => {
          return paper.rss_fetch_subject_id === this.selectedSubject.id;
        });
      }
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
  },
  methods: {
    getScrollTop() {
      const body = document.body;
      const html = document.documentElement;
      return body.scrollTop || html.scrollTop;
    },
    fetchPapers() {
      return axios.get('/api/papers', {
          params: {
            count: this.papers.length,
          },
      })
    },
    checkAndFetchPapers() {
      const html = document.documentElement;
      const scrollTop = this.getScrollTop();
      if (this.isFetchCompleted || this.inRequest || scrollTop / html.scrollHeight < 0.9) {
        return;
      }
      this.inRequest = true;
      this.fetchPapers().then(res => {
        this.inRequest = false;
        const papers = res.data.papers;
        if (papers.length === 0) {
          this.isFetchCompleted = true;
        } else {
          this.$emit('addPapers', papers);
        }
      }).catch(error => {
        this.inRequest = false;
        console.log(error);
      })
    },
    selectItem(paperId) {
      for (let paper of this.papers) {
        if (paper.id === paperId) {
          this.selectedPaper = paper;
          break;
        }
      }
    },
    closePaperModal() {
      this.selectedPaper = null;
    },
  },
};
</script>

<style lang="scss" scoped>
#paper-list {

  .paper-list-container {
    margin: 1em 1em 0;
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
