<template>
<div>
  <div class="tabs is-centered is-boxed">
    <ul>
      <li :class="{ 'is-active': !selectedSubject }">
        <a @click="selectSubject('')">
          All
        </a>
      </li>
      <li
        v-for="subject in subjects"
        :class="{ 'is-active': subject.name == selectedSubject }"
      >
        <a @click="selectSubject(subject.name)">
          {{ subject.name }}
        </a>
      </li>
    </ul>
  </div>
</div>
</template>

<script>
export default {
  props: {
    subjects: Array,
    selectedSubject: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
    };
  },
  methods: {
    selectSubject(subjectName) {
      this.$emit('selectSubject', subjectName);
    },
  }
};
</script>

<style lang="scss" scoped>
</style>
