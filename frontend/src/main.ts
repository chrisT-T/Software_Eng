import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import ArcoVue from "@arco-design/web-vue";
import ArcoVueIcon from "@arco-design/web-vue/es/icon";
import "@arco-design/web-vue/dist/arco.css";
import router from "./router";

createApp(App)
  .use(store)
  .use(router)
  .use(ElementPlus)
  .use(ArcoVue)
  .use(ArcoVueIcon)
  .mount("#app");
