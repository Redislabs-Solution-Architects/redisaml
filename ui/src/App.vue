<template>
  <div id="app">
    <Header/>
    <SearchForm v-on:search="search"/>
    <SearchResults
      v-if="results.length > 0"
      v-bind:results="results"
      v-bind:reformattedSearchString="reformattedSearchString"
    />
  </div>
</template>
<script>
import Header from './components/Header';
import SearchForm from './components/SearchForm';
import SearchResults from './components/SearchResults';
// import FileItem from './components/FileItem';
// import CaseItem from './components/CaseItem';
import axios from 'axios';

export default {
  name: 'app',
  components: {
    Header,
    SearchForm,
    SearchResults
    // ,
    // FileItem,
    // CaseItem
  },
  data() {
    return {
      results: [],
      reformattedSearchString: '',
      case_or_file: "case",
      resultCount: 25,
      caseSearchOptions: {
        val_min: 0,
        val_max: 10000000,
        investigator: null,
        status: null,
        priority: null,
        pri_acctno: null,
        related_tags: null,
        ssn: null
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
    search(searchParams, case_or_file) {
      this.reformattedSearchString = searchParams.join(' ');
      this.api.q = searchParams.join('+');
      console.log(searchParams)

      if (case_or_file == "case") {
        // this.case_or_file = "case";
        const { baseUrl, q} = this.api;
        const apiUrl = `${baseUrl}search?count=${this.resultCount}&search_str=${q}`;
        console.log(apiUrl);
        this.getData(apiUrl);
      } else {
        // this.case_or_file = "file";
        const { baseUrl, q} = this.api;
        const apiUrl = `${baseUrl}filesearch?count=${this.resultCount}&search_str=${q}`;
        console.log(apiUrl);
        this.getData(apiUrl);
      }

    },
    getData(apiUrl) {
      axios
        .get(apiUrl)
        .then(res => {
          this.results = res.data;
          console.log(res.data)
        })
        .catch(error => console.log(error));
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
