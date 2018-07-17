<template>
<div class="card filtering-card">
  <header class="card-header">
    <p class="card-header-title">
      絞り込み
    </p>
  </header>
  <div class="card-content">
    <div class="columns">
    <div class="column">
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">記事種別</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="selectedSubmitType" @change="selectSubmitType">
                <option>全て</option>
                <option v-for="submitType in submitTypes">{{ submitType.display_name }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">カテゴリ</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="selectedSubjectName" @change="selectSubject">
                <option>全て</option>
                <option v-for="subject in subjects">{{ subject.name }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">更新日</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow has-addons">
          <div class="control has-icons-left">
            <flat-pickr
              v-model="selectedDate"
              :config="flatPickrConfig"
              class="input"
              placeholder="対象の日付を選択"
            ></flat-pickr>
            <span class="icon is-small is-left">
              <i class="fa fa-calendar"></i>
            </span>
          </div>
          <div class="control">
            <a type="submit" class="button" @click="removeDate">
              <span class="icon is-small"><i class="fa fa-times-circle"></i></span>
            </a>
          </div>
        </div>
      </div>
    </div>
    </div>
    <div class="column">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">タイトル検索</label>
        </div>
        <div class="field-body">
          <div class="field is-expanded">
            <div class="field has-addons">
              <p class="control has-icons-left is-expanded">
                <input class="input" type="text" placeholder="スペース区切りで検索" v-model="searchQuery">
                <span class="icon is-small is-left">
                  <i class="fa fa-search"></i>
                </span>
              </p>
              <div class="control">
                <a class="button is-info" @click="searchTitle">検索</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    subjects: Array,
    submitTypes: Array,
    minDate: String,
    maxDate: String,
    defaultSubmitType: {
      type: Object,
      default: null,
    },
    defaultSubject: {
      type: Object,
      default: null,
    },
    defaultDate: {
      type: String,
      default: '',
    },
    defaultSearchQuery: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      selectedSubmitType: (this.defaultSubmitType) ? this.defaultSubmitType.display_name : '全て',
      selectedSubjectName: (this.defaultSubject) ? this.defaultSubject.name : '全て',
      selectedDate: this.defaultDate,
      searchQuery: this.defaultSearchQuery,
    };
  },
  watch: {
    defaultDate() {
      this.$set(this, 'selectedDate', this.defaultDate);
    },
    selectedDate() {
      if (this.selectedDate) {
        this.selectDate();
      }
    },
  },
  computed: {
    flatPickrConfig() {
      return {
        minDate: this.minDate,
        maxDate: this.maxDate,
      };
    },
  },
  methods: {
    selectSubmitType() {
      const query = Object.assign({}, this.$route.query, {
        submitType: this.selectedSubmitType,
      });
      if (query.submitType === '全て') {
        delete query.submitType;
      }
      this.$router.push({
        name: 'home',
        query: query,
      });
    },
    selectSubject() {
      const query = Object.assign({}, this.$route.query, {
        subject: this.selectedSubjectName,
      });
      if (query.subject === '全て') {
        delete query.subject;
      }
      this.$router.push({
        name: 'home',
        query: query,
      });
    },
    selectDate() {
      this.$router.push({
        name: 'home',
        query: Object.assign({}, this.$route.query, {
          date: this.selectedDate,
        }),
      });
    },
    searchTitle() {
      const query = Object.assign({}, this.$route.query, {
        query: this.searchQuery,
      });
      if (!this.searchQuery) {
        delete query.query;
      }
      this.$router.push({
        name: 'home',
        query: query,
      });
    },
    removeDate() {
      const query = Object.assign({}, this.$route.query);
      delete query.date;
      this.$router.push({
        home: 'home',
        query: query,
      });
    },
  }
};
</script>

<style lang="scss" scoped>
.filtering-card {
  margin-bottom: 1em;
}
</style>
