<template>
  <div>
    <div class="card-body">
      <h5 class="card-title">
        <a
          :href="'https://www.youtube.com/watch?v=' + file.id.fileId"
          class="card-link"
          target="_blank"
        >{{ file.snippet.title }}</a>
      </h5>
      <h6
        class="card-subtitle mb-2 text-muted"
      >{{ file.snippet.channelTitle }} | {{ file.snippet.publishedAt | formatDate }}</h6>
      <p class="card-text">{{ file.snippet.description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileItem',
  props: ['file']
};
</script>