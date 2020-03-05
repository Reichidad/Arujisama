import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const routerOptions = [
  { path: '/main', name: 'Login', component: 'Login' },
  { path: '/stamp', name: 'Stamp', component: 'Stamp' },
  { path: '/signuppage', name: 'Signup', component: 'Signup' },
  { path: '/Forget', name: 'Forget', component: 'Forget' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

export default new Router({
  mode: 'history',
  routes
})
