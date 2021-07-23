<template>
  <div class="search-view">

    <SearchForm v-on:search="search"/>
    <SearchResults
      v-bind:results="results"
      v-bind:resultsType="resultsType"
      v-bind:reformattedSearchString="reformattedSearchString"
      v-bind:resultsCount="resultsCount"
    />
    <!-- <SearchForm v-on:search="search"/>
    <SearchResults /> -->
  </div>
</template>

<script>
import SearchForm from '../components/SearchForm';
import SearchResults from '../components/SearchResults';
import axios from 'axios';

export default {
  name: 'Search',
  components: {
    SearchForm,
    SearchResults,
  },
  data() {
    return {
      results: [],
      reformattedSearchString: '',
      resultsType: '',
      resultLimit: 25,
      resultsCount: null,
      caseSearchOptions: {
        val_min: 0,
        val_max: 10000000,
        // investigator: null,
        // status: null,
        // priority: null,
        // pri_acctno: null,
        // related_tags: null,
        // ssn: null
      },
      fileSearchOptions: {
        filetype: null,
        caseid: null
      },      
      api: {
        baseUrl: 'http://localhost:5000/',
        q: ''
      }
    };
  },
  methods: {
    search(searchParams, searchType) {
      this.reformattedSearchString = searchParams.join(' ');
      this.api.q = searchParams.join('+');
      var apiUrl = "";

      this.resultsType = searchType;
      console.log("Search params:" + this.reformattedSearchString + ", searchType: " + this.resultsType);
      // console.log("caseSearchOptions: " + this.caseSearchOptions);
      // this.case_or_file = "file";
      const { baseUrl, q} = this.api;

      if (searchType == "case") {
        apiUrl = `${baseUrl}search?count=${this.resultLimit}&search_str=${q}`;
      } else if (searchType == "file") {
        apiUrl = `${baseUrl}filesearch?count=${this.resultLimit}&search_str=${q}`;
      } else {
        console.log("How did we get here? 451");
      }

      console.log(apiUrl);
      this.getData(apiUrl);

    },
    getData(apiUrl) {
      axios
        .get(apiUrl)
        .then(res => {
          if ('data' in res) {
            this.results = res.data.results;
            this.resultsCount = res.data.resultsCount;
            // console.log("resultsCount: " + res.data.resultsCount + " data: " + res.data.results)
            // console.log("resultsCount: " + this.resultsCount + " data: " + this.results)
          } 
        })
        .catch(error => console.log(error));
    }
  },
}
</script>
