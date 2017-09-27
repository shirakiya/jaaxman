<template>
<div class="paper-item" :class="{ 'is-selected': isSelected }">
  <div class="paper-item-selected" v-if="isSelected">
    <span class="icon"><i class="fa fa-caret-right"></i></span>
  </div>
  <div class="paper-item-content" v-on:click="handleItemClick">
    <div class="columns is-gapless" :style="{ 'margin-bottom': '.2em' }">
      <div class="column is-1">
        <span class="tag is-light">{{ rssFetchSubjectName }}</span>
      </div>
      <div class="column">
        <span class="paper-item-subtitle">[原文] {{ paper.title }}</span>
      </div>
    </div>
    <div class="paper-item-title">
      {{ paperTitleJa }}
    </div>
    <div class="paper-item-body">
      <div class="has-text-left">
        {{ paper.abstract_ja | truncate(55) }}
      </div>
      <div class="has-text-right">
        <google-attribution-short></google-attribution-short>
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

export default {
  components: {
    googleAttributionShort,
  },
  props: {
    paper: Object,
    subjects: Object,
    isSelected: Boolean,
  },
  data() {
    return {
    };
  },
  computed: {
    rssFetchSubjectName() {
      if (this.paper.rss_fetch_subject_id in this.subjects) {
        return this.subjects[this.paper.rss_fetch_subject_id].name;
      } else {
        return null;
      }
    },
    paperTitleJa() {
      return this.paper.title_ja.replace(/[（(].+[）)]$/, '').trim();
    },
    paperAbstractJa() {
      return this.paper.abstract_ja.truncate(20, '...')
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
    getRssFetchSubjectName(rssFetchSubjectId) {
      return (rssFetchSubjectId in subjects) ? subjects[rssFetchSubjectId].name : null;
    },
    handleItemClick() {
      this.$emit('selectItem', this.paper.id);
    },
  },
};
</script>

<style lang="scss" scoped>
.paper-item {
  padding: 1em 0 .5em;
  border-bottom: 1px solid lightgray;

  &.is-selected {
    display: flex;
    background-color: whitesmoke;
  }

  &:hover {
    background-color: whitesmoke;
  }

  .paper-item-selected {
    align-self: center;
    width: 20px;
  }

  .paper-item-content {
    cursor: pointer;
    width: 100%;
    padding-left: .5em;
    padding-right: 1.5em;

    span.paper-item-subtitle {
      color: #6E6E6E;
      word-break: break-word;
      font-size: .8em;
      font-weight: 400;
    }

    .paper-item-title {
      margin-bottom: .2em;
      font-size: 18px;
      font-weight: bold;
    }

    .paper-item-body {
      font-size: .8em;
    }

    .paper-item-footer {
      overflow: hidden;
      font-size: .8em;

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
