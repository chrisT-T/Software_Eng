import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
<<<<<<< HEAD
createApp(App)
  .use(store)
  .use(router)
  .use(ElementPlus, { size: "small", zIndex: 3000 })
=======
import ArcoVue from "@arco-design/web-vue";
import "@arco-design/web-vue/dist/arco.css";

createApp(App)
  .use(store)
  .use(router)
  .use(ElementPlus)
  .use(ArcoVue)
>>>>>>> main
  .mount("#app");
