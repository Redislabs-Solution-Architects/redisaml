<template>

  <div class="container mb-3">
    <div class="d-flex mb-3">
      <div class="mr-auto">
        <h5>Search Results for "{{ reformattedSearchString }}". <i>{{ resultsCount }}</i> records found.</h5>
      </div>
    </div>
    <div v-if="resultsCount > 0">
      <div v-if="resultsType === 'case'" class="mr-auto">
          <table class="table table-striped table-hover">
              <thead class="thead-dark">
                  <tr>
                      <th scope="col">#</th>
                      <th scope="col">Case ID</th>
                      <th scope="col">Inv. ID</th>
                      <th scope="col">Value</th>
                      <th scope="col">Priority</th>
                      <th scope="col">Status</th>
                      <th scope="col">Acct. #</th>
                      <th scope="col">SSN</th>
                      <th scope="col">Date Reported</th>
                  </tr>
              </thead>
              <tbody>
                  <template v-for="(result, index) in results">
                      <tr :key="index" @click="doit(index)">
                          <td>{{ index + 1 }} </td>
                          <td><a href="">{{ result.caseid }}</a></td>
                          <td>{{ result.investigator }}</td>
                          <td>{{ result.value | formatMoney}}</td>
                          <td>{{ result.priority }}</td>
                          <td>{{ result.status }}</td>
                          <td>{{ result.primary_acctno }}</td>
                          <td>{{ result.ssn }}</td>
                          <td>{{ result.date_reported | formatDate}}</td>
                          <!-- <td>{{ result. }}</td> -->
                      </tr>  
                  </template>
              </tbody>
          </table>
      </div>
      <div v-if="resultsType  === 'file'">
          <table class="table table-striped table-hover">
              <thead class="thead-dark">
                  <tr>
                      <th scope="col">#</th>
                      <th scope="col">File ID</th>
                      <th scope="col">Case ID</th>
                      <th scope="col">s3_url</th>
                      <th scope="col">Filetype</th>
                      <th scope="col">Date Reported</th>
                  </tr>
              </thead>
              <tbody>
                  <template v-for="(result, index) in results">
                      <tr :key="index" @click="doit(index)">
                          <td>{{ index + 1 }} </td>
                          <td><a href="">{{ result.guid }}</a></td>
                          <td>{{ result.caseid }}</td>
                          <td><a href="">{{ result.s3_url }}</a></td>
                          <td>{{ result.filetype }}</td>
                          <td>{{ result.date_added | formatDate}}</td>
                      </tr>  
                  </template>
              </tbody>
          </table>
      </div>
    </div>
  </div>


</template>

<script>
// import FileItem from './FileItem';
// import CaseItem from './CaseItem';

export default {
  name: 'SearchResults',
  components: {
  },
  data() {
    return {
      title: 'Search Results',
    };
  },
  methods: {
    doit (index)
    {
      console.log(index);
    }
  },
  props: ['results', 'reformattedSearchString','resultsType','resultsCount'],
};
</script>

<style scoped>
button:focus {
  box-shadow: none !important;
}

container mb-3{

}

.detail-row{
 margin: 120px;
 text-align: left;
 background-color: lightgray;
}
</style>