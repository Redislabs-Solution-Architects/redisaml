<template>
  <!-- <header> -->
    <nav class="navbar sticky navbar-expand-sm navbar-light bg-light mb-5">
      <div class="container">
        <a class="navbar-brand" href="#">
          <i class="fas fa-project-diagram" />
          <span class="ml-3">AML Case and File Search</span>
        </a>
        <div id="nav">
          <router-link to="/search">Search</router-link> |
          <router-link to="/about">About</router-link> |
          <router-link to="/info">Info</router-link>
        </div>
      </div>
    </nav>

  <!-- </header> -->
</template>

<script>

// import SearchForm from './SearchForm';
export default {
  name: 'Header',
  components: {
    // SearchForm,
  }  
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