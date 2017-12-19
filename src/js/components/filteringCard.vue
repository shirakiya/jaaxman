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
        <label class="label">Subject</label>
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
        <label class="label">Submit Type</label>
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
  </div>
</div>
</template>

<script>
export default {
  props: {
    subjects: Array,
    submitTypes: Array,
  },
  data() {
    return {
      selectedSubjectName: 'ALL',
      selectedSubmitType: 'ALL',
    };
  },
  methods: {
    selectSubject() {
      this.$emit('selectSubject', this.selectedSubjectName);
    },
    selectSubmitType() {
      this.$emit('selectSubmitType', this.selectedSubmitType);
    }
  }
};
</script>

<style lang="scss" scoped>
.filtering-card {
  margin-bottom: 1em;
}
</style>
