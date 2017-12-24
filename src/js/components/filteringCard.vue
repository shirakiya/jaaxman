<template>
<div class="card filtering-card">
  <header class="card-header">
    <p class="card-header-title">
      絞り込み
    </p>
  </header>
  <div class="card-content">
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">カテゴリ</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="selectedSubjectName" @change="selectSubject">
                <option>ALL</option>
                <option v-for="subject in subjects">{{ subject.name }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">記事種別</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="selectedSubmitType" @change="selectSubmitType">
                <option>ALL</option>
                <option v-for="submitType in submitTypes">{{ submitType.display_name }}</option>
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
          <div class="control has-icons-left" :class="{ 'is-loading': inDateRequest }">
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
</div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    subjects: Array,
    submitTypes: Array,
  },
  data() {
    return {
      selectedSubjectName: 'ALL',
      selectedSubmitType: 'ALL',
      inDateRequest: false,
      selectedDate: null,
      flatPickrConfig: {
        minDate: "2017-12",
      },
    };
  },
  watch: {
    selectedDate() {
      if (!this.selectedDate || this.inDateRequest) {
        return;
      }
      this.fetchPaperByDate(this.selectedDate);
    },
  },
  methods: {
    selectSubject() {
      this.$emit('selectSubject', this.selectedSubjectName);
    },
    selectSubmitType() {
      this.$emit('selectSubmitType', this.selectedSubmitType);
    },
    fetchPaperByDate(requestDate) {
      this.inDateRequest = true;

      axios.get('/api/papers', {
        params: {
          date: requestDate,
        }
      }).then(res => {
        this.inDateRequest = false;
        const papers = res.data.papers;
        if (papers && papers[requestDate]) {
          this.$emit('replacePapers', papers);
        }
      }).catch(error => {
        this.inDateRequest = false;
        console.error(error);
      })
    },
    removeDate() {
      this.selectedDate = null;
      this.$emit('undoPapers');
    },
  }
};
</script>

<style lang="scss" scoped>
.filtering-card {
  margin-bottom: 1em;
}
</style>
