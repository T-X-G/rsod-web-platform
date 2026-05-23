<template>
  <!-- 路由未就绪时显示空白背景（与登录页背景一致），避免闪烁 -->
  <div v-if="!isRouterReady" class="auth-bg"></div>
  <!-- 路由就绪后根据路径渲染 -->
  <template v-else>
    <router-view v-if="isAuthPage" />
    <MainLayout v-else>
      <template #sidebar>
        <Sidebar />
      </template>
      <template #header>
        <Header />
      </template>
      <template #content>
        <router-view />
      </template>
    </MainLayout>
  </template>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import MainLayout from "./layouts/MainLayout.vue";
import Sidebar from "./components/Sidebar.vue";
import Header from "./components/Header.vue";

const route = useRoute();
const router = useRouter();

// 路由就绪状态
const isRouterReady = ref(false);

const isAuthPage = computed(() => {
  const authPaths = ["/", "/login", "/register", "/forgot-password"];
  const currentPath = route.path || "";
  return authPaths.includes(currentPath);
});

onMounted(async () => {
  // 等待路由完全就绪，包括所有重定向
  await router.isReady();
  
  // 添加一个延迟，确保所有路由重定向都已完成
  await new Promise(resolve => setTimeout(resolve, 50));
  
  isRouterReady.value = true;
});
</script>

<style scoped>
.auth-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
}
</style>
