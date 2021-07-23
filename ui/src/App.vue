<template>
  <div id="app">
    <Header/>

    <router-view/>

    <Footer :api="api"/>
  </div>
</template>
<script>
import Header from './components/Header';
import Footer from './components/Footer';
// import axios from 'axios';

export default {
  name: 'app',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      // results: [],
      // reformattedSearchString: '',
      // resultsType: '',
      // resultLimit: 25,
      // caseSearchOptions: {
      //   val_min: 0,
      //   val_max: 10000000,
      //   // investigator: null,
      //   // status: null,
      //   // priority: null,
      //   // pri_acctno: null,
      //   // related_tags: null,
      //   // ssn: null
      // },
      // fileSearchOptions: {
      //   filetype: null,
      //   caseid: null
      // },      
      api: {
        baseUrl: 'http://localhost:5000/',
        q: ''
      }
    };
  },
  // methods: {
  //   search(searchParams, searchType) {
  //     this.reformattedSearchString = searchParams.join(' ');
  //     this.api.q = searchParams.join('+');
  //     var apiUrl = "";

  //     this.resultsType = searchType;
  //     console.log("Search params:" + this.reformattedSearchString + ", searchType: " + this.resultsType);
  //     // console.log("caseSearchOptions: " + this.caseSearchOptions);
  //     // this.case_or_file = "file";
  //     const { baseUrl, q} = this.api;

  //     if (searchType == "case") {
  //       apiUrl = `${baseUrl}search?count=${this.resultLimit}&search_str=${q}`;
  //     } else if (searchType == "file") {
  //       apiUrl = `${baseUrl}filesearch?count=${this.resultLimit}&search_str=${q}`;
  //     } else {
  //       console.log("How did we get here? 451");
  //     }

  //     console.log(apiUrl);
  //     this.getData(apiUrl);

  //     // console.log("Fetching index info...");
  //     // this.getData(this.api.baseUrl + "info/all")

  //   },
  //   getData(apiUrl) {
  //     axios
  //       .get(apiUrl)
  //       .then(res => {
  //         if ('data' in res) {
  //           this.results = res.data;
  //           console.log("Index data: " + res.data)
  //         } 
  //         // else {
  //         //   this.indexInfo = res.indeces;
  //         //   console.log("Index data: " + res.indices);
  //         // }

  //       })
  //       .catch(error => console.log(error));
  //   }

  // }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
