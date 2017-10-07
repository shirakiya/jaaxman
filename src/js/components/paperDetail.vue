<template>
<div id="paper-detail">
  <div>
    <div class="paper-detail-container selected" v-if="paper">
      <div class="paper-detail-header">
        <div class="paper-detail-header-right">
          <span class="tag is-light">{{ subject.name }}</span>
        </div>
        <div class="paper-detail-header-left">
          <span>更新日: {{ updateDate }}</span>
        </div>
      </div>
      <div class="paper-detail-title">
        <div class="paper-detail-maintitle">
          <a :href="paper.link" target="_blank">
            <p class="title is-4 has-text-gray-dark">{{ paper.title_ja }}</p>
          </a>
        </div>
        <div class="paper-detail-subtitle">
          <p class="title is-6 has-text-grey-dark">{{ paper.title }}</p>
        </div>
        <div class="paper-detail-anchortitle">
          <p class="subtitle is-6">
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
          <a class="button" :href="paper.link" target="_blank">
            <span class="icon"><i class="fa fa-link"></i></span>
            <span>論文ページへ</span>
          </a>
        </p>
      </div>
    </div>
    <div class="paper-detail-container not-selected" v-else>
      <p class="title is-2 has-text-centered"><span class="icon"><i class="fa fa-hand-o-left"></i></span>select paper...</p>
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
    subject: Object,
  },
  updated () {
    const paperDetailHeight = document.getElementById('paper-detail').clientHeight;
    this.$emit('updateHeight', paperDetailHeight);
  },
  computed: {
    authors() {
      return '著者';
    },
    updateDate() {
      return moment(this.paper.created_at).format('YYYY/MM/DD');
    },
  },
};
</script>

<style lang="scss" scoped>
#paper-detail {
  padding: 4em 3em 3em 2em;

  .paper-detail-container {

    .paper-detail-header {
      display: block;
      overflow: hidden;
      margin-bottom: .3em;

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
        }
      }

      .paper-detail-anchortitle {
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

    &.not-selected {
      p.title {
        span:first-child {
          margin-right: .5em;
        }
      }
    }
  }
}
</style>
