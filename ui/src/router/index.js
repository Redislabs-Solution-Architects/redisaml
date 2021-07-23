import Vue from 'vue'
import VueRouter from 'vue-router'
import Search from '../views/Search.vue'
import Info from '../views/Info.vue'
import About from '../views/About.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/info',
    name: 'Info',
    component: Info
  }
]

const router = new VueRouter({
  routes
})

export default router
