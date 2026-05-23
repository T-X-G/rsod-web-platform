import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "首页",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "登录",
    component: () => import("../views/LoginPage.vue"),
    meta: { requiresAuth: false, isAuthPage: true },
  },
  {
    path: "/register",
    name: "注册",
    component: () => import("../views/RegisterPage.vue"),
    meta: { requiresAuth: false, isAuthPage: true },
  },
  {
    path: "/forgot-password",
    name: "忘记密码",
    component: () => import("../views/ForgotPasswordPage.vue"),
    meta: { requiresAuth: false, isAuthPage: true },
  },
  {
    path: "/detection",
    name: "智能检测",
    component: () => import("../views/DetectionPage.vue"),
    meta: { requiresAuth: true, isAuthPage: false },
  },
  {
    path: "/history",
    name: "历史记录",
    component: () => import("../views/HistoryPage.vue"),
    meta: { requiresAuth: true, isAuthPage: false },
  },
  {
    path: "/qa",
    name: "AI问答",
    component: () => import("../views/QAPage.vue"),
    meta: { requiresAuth: true, isAuthPage: false },
  },
  {
    path: "/targets",
    name: "目标库",
    component: () => import("../views/TargetsPage.vue"),
    meta: { requiresAuth: true, isAuthPage: false },
  },
  {
    path: "/profile",
    name: "个人中心",
    component: () => import("../views/ProfilePage.vue"),
    meta: { requiresAuth: true, isAuthPage: false },
  },
  {
    path: "/settings",
    name: "系统设置",
    component: () => import("../views/Settings.vue"),
    meta: { requiresAuth: true, isAuthPage: false },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 使用同步路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  
  // 如果是公开页面（不需要认证），直接放行
  if (to.meta.requiresAuth === false) {
    // 如果已登录用户访问登录页，重定向到主页面
    if (token && to.path === "/login") {
      next("/detection");
      return;
    }
    next();
    return;
  }

  // 需要认证的页面
  if (!token) {
    next("/login");
    return;
  }

  next();
});

export default router;
