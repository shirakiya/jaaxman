<template>
<div class="modal" :class="{ 'is-active': isActive }">
  <div class="modal-background" @click="closeModal"></div>
  <div class="modal-card">
    <section class="modal-card-body paper-detail-container">
      <div class="paper-detail-header">
        <div class="paper-detail-header-right">
          <a class="button is-small" @click="closeModal">
            <span class="icon"><i class="fas fa-arrow-left" aria-hidden="true"></i></span>
            <span>戻る</span>
          </a>
        </div>
        <div class="paper-detail-header-left">
          <span class="tag is-success">
            {{ paper.submit_type }}
          </span>
          <span class="tag is-warning">
            <a class="has-text-black-bis" :href="subjectUrl" target="_blank">
              {{ subject.name }}
            </a>
          </span>
          <span>更新日: {{ updateDate }}</span>
        </div>
      </div>
      <div class="paper-detail-title">
        <div class="paper-detail-maintitle">
          <a :href="paper.link" target="_blank">
            <p class="title is-5 has-text-gray-dark">{{ paper.title_ja }}</p>
          </a>
        </div>
        <div class="paper-detail-subtitle">
          <p class="title has-text-grey-dark">原文: {{ paper.title }}</p>
        </div>
        <div class="paper-detail-anchortitle">
          <p class="subtitle">
          著者: <span class="paper-detail-author" v-for="author in paper.authors">
            <a :href="author.link" target="_blank">{{ author.name }}</a>
          </span>
          </p>
        </div>
      </div>
      <div class="paper-detail-body-main">
        <p class="has-text-centered">［要約］</p>
        <p class="has-text-gray">{{ paper.abstract_ja }}</p>
      </div>
      <div class="paper-detail-body-sub">
        <p class="has-text-centered">［ABSTRACT］</p>
        <p class="has-text-gray">{{ paper.abstract }}</p>
      </div>
      <div class="paper-detail-footer">
        <p class="has-text-right">
          <google-attribution-short :width="150"></google-attribution-short>
        <p>
        <p class="has-text-centered">
          <a class="button is-primary" :href="paper.link" target="_blank">
            <span class="icon"><i class="fa fa-link"></i></span>
            <span>論文ページへ</span>
          </a>
        </p>
      </div>
    </section>
  </div>
  <button class="modal-close is-large" aria-label="close" @click="closeModal"></button>
</div>
</template>

<script>
import moment from 'moment';
import googleAttributionShort from './googleAttributionShort.vue';
import { getSubjectPageUrl } from './../utils/arxiv.js';

export default {
  props: {
    paper: Object,
    subject: Object,
    isActive: Boolean,
  },
  components: {
    googleAttributionShort,
  },
  data() {
    return {
    };
  },
  computed: {
    updateDate() {
      return moment(this.paper.created_at).format('YYYY/MM/DD');
    },
    subjectUrl() {
      return getSubjectPageUrl(this.subject.name);
    },
  },
  methods: {
    closeModal() {
      const query = Object.assign({}, this.$route.query);
      delete query.paperId;
      this.$router.push({
        name: 'home',
        query: query,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.paper-detail-container {

  .paper-detail-header {
    display: block;
    overflow: hidden;
    margin-bottom: 1em;

    .paper-detail-header-right {
      float: left;
    }

    .paper-detail-header-left {
      float: right;
    }
  }

  .paper-detail-title {
    margin: .5em 0 1em;

    .paper-detail-maintitle {
      margin-bottom: .5em;
    }

    .paper-detail-subtitle {
      margin: .3em 0 .5em;

      p.title {
        margin-bottom: .3em;
        font-size: .88rem;
      }
    }

    .paper-detail-anchortitle {

      p.subtitle {
        font-size: .88rem;
      }

      span {
        &.paper-detail-author {
          &:first-child {
            padding-left: .2em;
          }

          &:after {
            padding-left: .5em;
            padding-right: .5em;
            content: "/";
          }

          &:last-child {
            &:after {
              padding-left: 0;
              padding-right: 0;
              content: none;
            }
          }
        }
      }
    }
  }

  .paper-detail-body-main {
    word-break: break-word;
    font-size: 1em;
    line-height: 1.5;
    font-weight: 400;
    margin: .5em 0;
  }

  .paper-detail-body-sub {
    word-break: break-word;
    font-size: .9em;
    line-height: 1.8;
    font-weight: 400;
    margin: .5em 0;
    padding-top: .8em;
    border-top: 1px dashed lightgray;
  }

  .paper-detail-footer {
    margin-top: 1em;
  }
}
</style>
