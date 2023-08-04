import Vue from "vue"
import App from "./App.vue"
import instance from "./utils/util"
import ElementUI from "element-ui"
import "element-ui/lib/theme-chalk/index.css"
import locale from 'element-ui/lib/locale/lang/en'


import VueSocialauth from "vue-social-auth";
Vue.use(VueSocialauth, {
  providers: {
    facebook: {
      clientId: "659715154536727",
      redirectUri:
        "http://cryptic-bayou-98994.herokuapp.com/api/user/login/facebook"
    },
    google: {
      clientId:"1029286495108-3107mjncjooi9mta6pngt74rqos3811l.apps.googleusercontent.com",
      redirectUri:"http://localhost:8080"
    }
  }
});


Vue.use(ElementUI, { locale })

Vue.config.productionTip = false
Vue.prototype.$http = instance


new Vue({
  render: (h) => h(App)
}).$mount("#app")
