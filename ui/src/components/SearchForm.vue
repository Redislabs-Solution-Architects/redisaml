<template>
  <div class="container">
    <form class="mb-5">
      <div class="input-group">
        <input
          v-model="searchString"
          @keydown.13.prevent="parseSearchString"
          type="text"
          class="form-control"
          placeholder="Search ...: <terms> @investigator:{ } @priority:{ } @status:{ } @primary_acctno:{ } @related_tags:{ } @ssn:{ }"
        >
        <div class="input-group-append">
          <button @click="parseSearchString" class="btn btn-outline-secondary" type="button">
            <i class="fas fa-search"></i>
          </button>
        </div>
      </div>
      <div class="container">
        <input type="radio" id="case" value="case" v-model="picked"> cases
        <input type="radio" id="file" value="file" v-model="picked"> files
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SearchForm',
  data() {
    return {
      picked: "case",
      searchString: ''
    };
  },
  methods: {
    parseSearchString() {
      // Trim search string
      const trimmedSearchString = this.searchString.trim();

      if (trimmedSearchString !== '') {
        // Split search string
        const searchParams = trimmedSearchString.split(/\s+/);
        
        // Emit event
        this.$emit('search', searchParams, this.picked);
        // Reset input field
        this.searchString = '';
      }
    }
  }
};
</script>

<style scoped>
input,
button{
  box-shadow: none !important;
  margin: 2px
}

.radio {
    margin: 4px
}
.form-control {
  border-color: #6c757d;
}
</style>