import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/login",
    meta: {
      LoginRequired: false,
    },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
    meta: {
      LoginRequired: false,
    },
  },
  {
    path: "/main/:username",
    name: "main",
    component: () => import("../views/MainView.vue"),
    meta: {
      LoginRequired: true,
    },
  },
  {
    path: "/coding/:username/:projectid",
    name: "coding",
    component: () => import("../views/CodingView.vue"),
    meta: {
      LoginRequired: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.LoginRequired) {
    const username = sessionStorage.getItem("username");
    if (username) {
      if (to.params.username == username) {
        next();
      } else {
        router.replace({ name: "main", params: { username: username } });
      }
    } else {
      next({
        path: "/login",
        query: { redirected: to.fullPath },
      });
    }
  } else if (to.name == "login") {
    const username = sessionStorage.getItem("username");
    if (username) {
      router.replace({ name: "main", params: { username: username } });
    } else next();
  } else next();
});

export default router;
