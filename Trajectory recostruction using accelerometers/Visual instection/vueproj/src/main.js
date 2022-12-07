import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import VueGoodTablePlugin from 'vue-good-table'
import Verte from 'verte'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-good-table/dist/vue-good-table.css'
import 'verte/dist/verte.css'


Vue.component('verte', Verte);

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueGoodTablePlugin)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
