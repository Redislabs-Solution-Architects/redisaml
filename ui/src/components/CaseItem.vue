<template>
  <div>
    <div class="card-body">
      <!-- <h5 class="card-title">
        <a
          :href="'https://www.youtube.com/watch?v=' + case.id.caseId"
          class="card-link"
          target="_blank"
        >{{ case.snippet.title }}</a>
      </h5>
      <h6
        class="card-subtitle mb-2 text-muted"
      >{{ case.snippet.channelTitle }} | {{ case.snippet.publishedAt | formatDate }}</h6>
      <p class="card-text">{{ case.snippet.description }}</p> -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'CaseItem',
  props: ['case']
};
</script>