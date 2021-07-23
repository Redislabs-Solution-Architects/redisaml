<template>

      <div class="container" :indexInfo="indexInfo">
        <hr />
        <div v-if="indexInfo">
          Cases: {{ indexInfo.cases.num_docs }}, Files: {{ indexInfo.files.num_docs }}
        </div>
      </div>

</template>

<script>

export default {
  name: 'Footer',
  data() {
    return {
      indexInfo: {
        cases: {
          num_docs: null,
        },
        files: {
          num_docs: null,
        }
      },
    }
  },
  methods: {
    async getInfo() {
      const res = await fetch(this.api.baseUrl + "/info/all");
      this.indexInfo = await res.json();
    }
  },
  mounted() {
    this.getInfo()
  },
  props: ['api'],  
};
</script>

<style scoped>
</style>