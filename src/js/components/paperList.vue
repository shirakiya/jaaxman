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
      <div id='paper-list-content' :style="paperListContentStyle">
        <paper-item v-for="paper in filteredPapers" :paper="paper" :subjects="subjects" :key="paper.id"></paper-item>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import paperItem from './paperItem.vue';

export default {
  props: {
    subjects: Object,
    papers: Array,
  },
  components: {
    paperItem,
  },
  mounted() {
    this.setPaperListContentStyle();
    window.addEventListener('resize', this.setPaperListContentStyle);
  },
  bedoreDestory() {
    window.removeEventListener('resize', this.setPaperListContentStyle);
  },
  data() {
    return {
      selectedTab: '',
      paperListContentHeight: '100%',
    };
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
    setPaperListContentStyle(e) {
      const clientHeight = document.documentElement.clientHeight;
      const rect = document.getElementById('paper-list-content').getBoundingClientRect();
      this.paperListContentHeight = clientHeight - rect.top + 'px';
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
    }
  }
}
</style>
