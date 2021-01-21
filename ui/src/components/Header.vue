<template>
  <header>
    <nav class="navbar navbar-expand-sm navbar-dark bg-dark mb-5">
      <div class="container">
        <a class="navbar-brand" href="#">
          <i class="fab fa-cc-discover fa-2x"></i>
          <span class="ml-3">AML Case and File Search</span>
        </a>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'Header'
};
</script>

<style scoped>
i {
  vertical-align: middle;
  color: orange;
}

i + span {
  vertical-align: middle;
}
</style>