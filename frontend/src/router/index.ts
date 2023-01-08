import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import axios from "axios";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/login",
    meta: {
      title: "TOCODE | Login",
      LoginRequired: false,
    },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
    meta: {
      title: "TOCODE | Login",
      LoginRequired: false,
    },
  },
  {
    path: "/main/:username",
    name: "main",
    component: () => import("../views/MainView.vue"),
    meta: {
      title: "TOCODE | Project Management",
      LoginRequired: true,
    },
  },
  {
    path: "/coding/:username/:projectid",
    name: "coding",
    component: () => import("../views/CodingView.vue"),
    meta: {
      title: "TOCODE | Coding",
      LoginRequired: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const username = localStorage.getItem("username");
  console.log(localStorage.getItem("username"));
  if (username) {
    const activeTime = Number(localStorage.getItem("active_time"));
    const time = new Date().getTime();
    if (time - activeTime > 1800000 && activeTime != 0) {
      localStorage.removeItem("username");
      localStorage.removeItem("active_time");
      axios.get("/api/logout");
      router.replace("/login");
    } else {
      if (to.name == "login") {
        router.replace({ name: "main", params: { username: username } });
      }
      if (to.params.username == username) {
        next();
      } else {
        router.replace({ name: "main", params: { username: username } });
      }
    }
  } else {
    if (to.name !== "login") {
      next({
        path: "/login",
        query: { redirected: to.fullPath },
      });
    } else {
      next();
    }
  }
});

export default router;
