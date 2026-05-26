import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import App from "./App.vue";
import "./assets/main.css";

// Public Pages
import HomePage from "./views/HomePage.vue";
import LoginPage from "./views/LoginPage.vue";
import ForgotPassword from "./views/ForgotPassword.vue";

// Dashboard Pages
import DetectionPage from "./views/DetectionPage.vue";
import HistoryPage from "./views/HistoryPage.vue";
import AIChatPage from "./views/AIChatPage.vue";
import TargetsPage from "./views/TargetsPage.vue";
import ProfilePage from "./views/ProfilePage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Public routes
    { path: "/", name: "home", component: HomePage },
    { path: "/login", name: "login", component: LoginPage },
    { path: "/register", name: "register", component: LoginPage },
    {
      path: "/forgot-password",
      name: "forgot-password",
      component: ForgotPassword,
    },

    // Dashboard routes
    { path: "/dashboard", redirect: "/dashboard/detection" },
    {
      path: "/dashboard/detection",
      name: "detection",
      component: DetectionPage,
    },
    { path: "/dashboard/history", name: "history", component: HistoryPage },
    { path: "/dashboard/ai-chat", name: "ai-chat", component: AIChatPage },
    { path: "/dashboard/targets", name: "targets", component: TargetsPage },
    { path: "/dashboard/profile", name: "profile", component: ProfilePage },
  ],
});

const app = createApp(App);
const pinia = createPinia();
app.use(router);
app.use(pinia);
app.mount("#app");
