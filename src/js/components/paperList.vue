<template>
<div id="paper-list">
  <div class="paper-list-container">
    <div class="tabs is-centered">
      <ul>
        <li :class="{ 'is-active': !selectedTab }">
          <a @click="selectTab('')">All</a>
        </li>
        <li v-for="subject in subjects" :class="{ 'is-active': selectedTab === subject.name }">
          <a @click="selectTab(subject.name)">{{ subject.name }}</a>
        </li>
      </ul>
    </div>
    <div class="paper-list-main">
      <div class="paper-list-title">
        <h3 class="title" v-if="!selectedTab">
          All
        </h3>
        <h3 class="title is-3" v-else>
          <a :href="tabUrl" target="_blank">
            {{ selectedTab }}
          </a>
        </h3>
      </div>
      <div id='paper-list-content' class="paper-list-content" :style="paperListContentStyle">
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
  </div>
</div>
</template>

<script>
import paperItem from './paperItem.vue';
import axios from 'axios';

export default {
  props: {
    subjects: Object,
    papers: Array,
    selectedPaper: {
      type: Object,
      required: false,
    },
    paperDetailHeight: Number,
  },
  components: {
    paperItem,
  },
  mounted() {
    this.setPaperListContentStyle();
    window.addEventListener('resize', this.setPaperListContentStyle);
    const paperListContent = document.getElementById('paper-list-content');
    paperListContent.addEventListener('scroll', this.fetchPapers);
  },
  bedoreDestory() {
    window.removeEventListener('resize', this.setPaperListContentStyle);
    const paperListContent = document.getElementById('paper-list-content');
    paperListContent.removeEventListener('scroll', this.fetchPapers);
  },
  data() {
    return {
      selectedTab: '',
      paperListContentHeight: '100%',
      inRequest: false,
      isFetchCompleted: false,
    };
  },
  watch: {
    paperDetailHeight() {
      this.setPaperListContentStyle();
    },
  },
  computed: {
    tabUrl() {
      return 'https://arxiv.org/list/' + this.selectedTab + '/recent';
    },
    paperListContentStyle() {
      return {
        overflow: 'scroll',
        height: this.paperListContentHeight,
      }
    },
    filteredPapers() {
      if (this.selectedTab === '') {
        return this.papers;
      }
      else {
        return this.papers.filter((paper) => {
          return this.subjects[paper.rss_fetch_subject_id].name === this.selectedTab;
        });
      }
    },
  },
  methods: {
    selectTab(tab) {
      this.selectedTab = tab;
    },
    setPaperListContentStyle() {
      const clientHeight = document.documentElement.clientHeight;
      const wholePaperDetailHeight = this.paperDetailHeight + 52;  // navbar
      const targetHeight = (clientHeight >= wholePaperDetailHeight) ? clientHeight : wholePaperDetailHeight;

      const paperListContent = document.getElementById('paper-list-content');
      let baseHeight;
      if ('offsetTop' in paperListContent) {
        baseHeight = paperListContent.offsetTop;
      } else {
        baseHeight = paperListContent.getBoundingClientRect().top;
      }

      this.paperListContentHeight = targetHeight - baseHeight + 'px';
    },
    fetchPapers() {
      const paperListContent = document.getElementById('paper-list-content');
      if (this.isFetchCompleted || this.inRequest || paperListContent.scrollTop / paperListContent.scrollHeight < 0.9) {
        return;
      } else {
        this.inRequest = true;
        axios.get('/api/papers', {
            params: {
              count: this.papers.length,
            },
          })
          .then(res => {
            this.inRequest = false;
            if (res.data.papers.length === 0) {
              this.isFetchCompleted = true;
            } else {
              this.$emit('addPapers', res.data.papers);
            }
          })
          .catch(error => {
            console.log(error);
            this.inRequest = false;
          })
      }
    },
    selectItem(paperId) {
      this.$emit('selectItem', paperId);
    },
  },
};
</script>

<style lang="scss" scoped>
#paper-list {
  border-right: 2px solid lightgray;

  .paper-list-container {
    padding-top: 1em;

    .paper-list-main {
      padding-left: 2em;

      .paper-list-title {
        padding-bottom: 0.5em;
      }

      .paper-list-content {

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
  }
}
</style>
