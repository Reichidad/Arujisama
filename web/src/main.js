// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import Meta from 'vue-meta'


// Vue.config.productionTip = false

axios.interceptors.request.use(function (config) {
  const token = localStorage.getItem('token');
  config.headers.Authorization = token;

  return config;
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  Meta,
  components: { App },
  render(h) {
    return h('App')
  }
})