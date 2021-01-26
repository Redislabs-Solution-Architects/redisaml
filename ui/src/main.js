import Vue from 'vue'
import App from './App.vue'
import moment from 'moment'

Vue.config.productionTip = false

Vue.filter('formatDate', function (value) {
  if (!value) return ''
  return moment.unix(value.toString()).format('MM/DD/YYYY hh:mm')
})

Vue.filter('formatMoney', function (value) {
  var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  
    // These options are needed to round to whole numbers if that's what you want.
    minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
    maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
  });
  if (!value) return ''
  return formatter.format(value)
})

new Vue({
  render: h => h(App),
}).$mount('#app')