<template>
  <div class="container mb-3">
    <div class="d-flex mb-3">
      <div class="mr-auto">
        <h3>Search Results for "{{ reformattedSearchString }}"</h3>
      </div>
      <!-- <div class="btn-group ml-auto" role="group">
        <button
          @click="changeDisplayMode('grid')"
          type="button"
          class="btn btn-outline-secondary"
          v-bind:class="{ active: displayMode === 'grid' }"
        >
          <i class="fas fa-th"></i>
        </button>
        <button
          @click="changeDisplayMode('list')"
          type="button"
          class="btn btn-outline-secondary"
          v-bind:class="{ active: displayMode === 'list' }"
        >
          <i class="fas fa-list"></i>
        </button>
      </div> -->
    </div>

    <div class="card-columns" v-if="case_or_file === 'file'">
      <div class="card" v-bind:key="result.id" v-for="result in results">
          File Search!
        <!-- <VideoGridItem v-bind:video="video"/> -->
        <CaseItem />
      </div>
    </div>
    <div v-if="case_or_file === 'case'">
      <div class="card mb-2" v-bind:key="result.id" v-for="result in results">
          Case Search!
        <!-- <VideoListItem v-bind:video="video"/> -->
        <FileItem />
      </div>
    </div>
    <div v-else>
        File or Case search not set!
    </div>
  </div>
</template>

<script>
import FileItem from './FileItem';
import CaseItem from './CaseItem';

export default {
  name: 'SearchResults',
  components: {
    FileItem,
    CaseItem
  },
  data() {
    return {
        // case_or_file: null,
      title: 'Search Results',
    //   displayMode: 'grid'
    };
  },
  methods: {
    // changeDisplayMode(displayMode) {
    //   this.displayMode = displayMode;
    // }
  },
  props: ['results', 'reformattedSearchString','case_or_file']
};
</script>

<style scoped>
button:focus {
  box-shadow: none !important;
}
</style>