<template>
<div class="paper-item" :class="{ 'is-selected': isSelected }">
  <div class="paper-item-content" v-on:click="handleItemClick">
    <div class="tags paper-item-header">
      <span class="tag is-success">
        {{ paper.submit_type }}
      </span>
      <span class="tag is-warning">
        <a class="has-text-black-bis" :href="subjectUrl" target="_blank">
          {{ rssFetchSubjectName }}
        </a>
      </span>
      <span class="paper-item-subtitle">[原文] {{ paper.title }}</span>
    </div>
    <div class="paper-item-title">
      {{ paperTitleJa }}
    </div>
    <div class="paper-item-body">
      <div class="has-text-left">
        {{ paper.abstract_ja | truncate(150) }}
      </div>
    </div>
    <div class="paper-item-footer">
      <div class="paper-item-footer-left">
        <span class="paper-item-author" v-if="isExistAuthor">
          <span class="icon"><i class="fa fa-user-circle-o"></i></span>
          <a :href="firstAuthor.link" target="_blank">
            {{ firstAuthor.name }}
          </a>
          <span v-if="isMultiAuthor">他</span>
        </span>
      </div>
      <div class="paper-item-footer-right">
        <span class="paper-item-link">
          <a :href="paper.link" target="_blank">
            <span class="icon"><i class="fa fa-link"></i></span>論文ページ
          </a>
        </span>
        <span class="paper-date">更新日: {{ updateDate }}</span>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import moment from 'moment';
import googleAttributionShort from './googleAttributionShort.vue';
import { getSubjectPageUrl } from './../utils/arxiv.js';

export default {
  components: {
    googleAttributionShort,
  },
  props: {
    paper: Object,
    subjects: Array,
    isSelected: {
      type: Boolean,
      default: false,
    },
  },
  data () {
    return {
    };
  },
  computed: {
    subjectUrl() {
      return getSubjectPageUrl(this.rssFetchSubjectName);
    },
    rssFetchSubjectName() {
      for (let subject of this.subjects) {
        if (subject.id === this.paper.rss_fetch_subject_id) {
          return subject.name;
        }
      }
      return null;
    },
    paperTitleJa() {
      return this.paper.title_ja.replace(/[（(].+[）)]$/, '').trim();
    },
    isExistAuthor() {
      return this.paper.authors.length > 0;
    },
    isMultiAuthor() {
      return this.paper.authors.length > 1;
    },
    firstAuthor() {
      return (this.paper.authors.length > 0) ? this.paper.authors[0] : null;
    },
    updateDate() {
      return moment(this.paper.created_at).format('YYYY/MM/DD');
    },
  },
  methods: {
    handleItemClick() {
      this.$emit('selectItem', this.paper.id);
    },
  },
};
</script>

<style lang="scss" scoped>
.paper-item {
  padding: 1.2em 0 .5em;
  border-bottom: 1px solid lightgray;

  &:first-child {
    padding: 0 0 .5em;
  }

  &.is-selected {
    background-color: whitesmoke;
  }

  &:hover {
    background-color: whitesmoke;
  }

  .paper-item-content {
    cursor: pointer;
    width: 100%;
    padding-left: .5em;
    padding-right: 1.5em;

    .paper-item-header {
      margin-bottom: .2em;
    }

    span.paper-item-subtitle {
      color: #6E6E6E;
      word-break: break-word;
      font-size: .7rem;
      font-weight: 400;
    }

    .paper-item-title {
      margin-bottom: .2em;
      font-size: 18px;
      font-weight: bold;
    }

    .paper-item-body {
      margin: .4em 0;
      font-size: .7rem;
    }

    .paper-item-footer {
      overflow: hidden;
      font-size: .7rem;

      .paper-item-footer-left {
        float: left;
      }

      .paper-item-footer-right {
        float: right;
      }
    }
  }

  .paper-item-author {
    margin-right: .5em;
  }

  .paper-item-link {
    margin: 1em;
  }
}
</style>
