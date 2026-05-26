<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import ParticleBackground from "../components/ParticleBackground.vue";
import LogoIcon from "../components/LogoIcon.vue";

const route = useRoute();
const router = useRouter();

const isRegister = computed(() => route.path === "/register");
const isVisible = ref(false);

const form = ref({
  username: "",
  password: "",
  confirmPassword: "",
  email: "",
  captcha: "",
});

const showPassword = ref(false);
const isLoading = ref(false);
const rememberMe = ref(false);

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
  }, 100);
});

import { login, register } from '../api/auth'

const handleSubmit = async () => {
  isLoading.value = true
  try {
    if (isRegister.value) {
      const res = await register(form.value.username, form.value.password, form.value.email || undefined)
      if (res.success) {
        localStorage.setItem('token', res.data.access_token)
        router.push('/dashboard/detection')
      } else {
        alert(res.message || '注册失败')
      }
    } else {
      const res = await login(form.value.username, form.value.password)
      if (res.success) {
        localStorage.setItem('token', res.data.access_token)
        router.push('/dashboard/detection')
      } else {
        alert(res.message || '登录失败')
      }
    }
  } catch {
    alert('网络错误，请检查后端服务是否运行')
  } finally {
    isLoading.value = false
  }
};

const goBack = () => {
  router.push("/");
};

const toggleMode = () => {
  router.push(isRegister.value ? "/login" : "/register");
};
</script>

<template>
  <div
    class="min-h-screen bg-background relative overflow-hidden flex items-center justify-center"
  >
    <!-- Background Effects -->
    <ParticleBackground />
    <div class="absolute inset-0 grid-pattern opacity-30"></div>

    <!-- Gradient Orbs -->
    <div
      class="absolute top-0 right-0 w-96 h-96 bg-primary/10 rounded-full blur-3xl"
    ></div>
    <div
      class="absolute bottom-0 left-0 w-80 h-80 bg-accent/10 rounded-full blur-3xl"
    ></div>

    <!-- Content -->
    <div
      class="relative z-10 w-full max-w-md mx-4"
      :class="{
        'opacity-0 translate-y-8': !isVisible,
        'opacity-100 translate-y-0': isVisible,
      }"
      style="transition: all 0.6s ease-out"
    >
      <!-- Back Button -->
      <button
        @click="goBack"
        class="absolute -top-12 left-0 flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors"
      >
        <svg
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 19l-7-7m0 0l7-7m-7 7h18"
          />
        </svg>
        返回首页
      </button>

      <!-- Login Card -->
      <div class="glass-card p-8 rounded-2xl shadow-card">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="flex justify-center mb-4">
            <div
              class="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/30 flex items-center justify-center"
            >
              <LogoIcon class="w-10 h-10" />
            </div>
          </div>
          <h1 class="text-2xl font-bold text-foreground mb-2">
            {{ isRegister ? "创建账号" : "欢迎回来" }}
          </h1>
          <p class="text-muted-foreground">
            {{
              isRegister
                ? "注册钢铁表面缺陷智能检测平台"
                : "登录钢铁表面缺陷智能检测平台"
            }}
          </p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- Username -->
          <div class="space-y-2">
            <label
              class="text-sm font-medium text-foreground flex items-center gap-2"
            >
              <svg
                class="w-4 h-4 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
              用户名
            </label>
            <input
              v-model="form.username"
              type="text"
              placeholder="请输入用户名"
              class="w-full px-4 py-3 bg-input border border-border rounded-xl text-foreground placeholder-muted-foreground focus:outline-none input-glow transition-all"
              required
            />
          </div>

          <!-- Email (Register only) -->
          <div v-if="isRegister" class="space-y-2">
            <label
              class="text-sm font-medium text-foreground flex items-center gap-2"
            >
              <svg
                class="w-4 h-4 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
              邮箱
            </label>
            <input
              v-model="form.email"
              type="email"
              placeholder="请输入邮箱地址"
              class="w-full px-4 py-3 bg-input border border-border rounded-xl text-foreground placeholder-muted-foreground focus:outline-none input-glow transition-all"
              required
            />
          </div>

          <!-- Password -->
          <div class="space-y-2">
            <label
              class="text-sm font-medium text-foreground flex items-center gap-2"
            >
              <svg
                class="w-4 h-4 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
              密码
            </label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入密码"
                class="w-full px-4 py-3 pr-12 bg-input border border-border rounded-xl text-foreground placeholder-muted-foreground focus:outline-none input-glow transition-all"
                required
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary transition-colors"
              >
                <svg
                  v-if="!showPassword"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>
          </div>

          <!-- Confirm Password (Register only) -->
          <div v-if="isRegister" class="space-y-2">
            <label
              class="text-sm font-medium text-foreground flex items-center gap-2"
            >
              <svg
                class="w-4 h-4 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                />
              </svg>
              确认密码
            </label>
            <input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              class="w-full px-4 py-3 bg-input border border-border rounded-xl text-foreground placeholder-muted-foreground focus:outline-none input-glow transition-all"
              required
            />
          </div>

          <!-- Captcha -->
          <div class="space-y-2">
            <label
              class="text-sm font-medium text-foreground flex items-center gap-2"
            >
              <svg
                class="w-4 h-4 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              验证码
            </label>
            <div class="flex gap-3">
              <input
                v-model="form.captcha"
                type="text"
                placeholder="请输入验证码"
                class="flex-1 px-4 py-3 bg-input border border-border rounded-xl text-foreground placeholder-muted-foreground focus:outline-none input-glow transition-all"
                required
              />
              <div
                class="w-28 h-12 bg-muted rounded-xl flex items-center justify-center text-primary font-mono text-lg cursor-pointer hover:bg-muted/80 transition-colors select-none"
              >
                A7K9
              </div>
            </div>
          </div>

          <!-- Remember Me / Forgot Password (Login only) -->
          <div
            v-if="!isRegister"
            class="flex items-center justify-between text-sm"
          >
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="w-4 h-4 rounded border-border bg-input text-primary focus:ring-primary focus:ring-offset-0"
              />
              <span class="text-muted-foreground">记住我</span>
            </label>
            <router-link
              to="/forgot-password"
              class="text-primary hover:text-primary/80 transition-colors"
              >忘记密码？</router-link
            >
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="btn-glow w-full py-4 bg-primary text-primary-foreground font-semibold rounded-xl shadow-glow hover:shadow-glow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <svg
              v-if="isLoading"
              class="w-5 h-5 animate-spin"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            {{ isLoading ? "处理中..." : isRegister ? "立即注册" : "登录" }}
          </button>
        </form>

        <!-- Divider -->
        <div class="flex items-center gap-4 my-6">
          <div class="flex-1 h-px bg-border"></div>
          <span class="text-muted-foreground text-sm">或</span>
          <div class="flex-1 h-px bg-border"></div>
        </div>

        <!-- Toggle Mode -->
        <div class="text-center">
          <span class="text-muted-foreground">
            {{ isRegister ? "已有账号？" : "还没有账号？" }}
          </span>
          <button
            @click="toggleMode"
            class="text-primary hover:text-primary/80 font-medium ml-1 transition-colors"
          >
            {{ isRegister ? "立即登录" : "立即注册" }}
          </button>
        </div>
      </div>

      <!-- Security Notice -->
      <div
        class="mt-6 flex items-center justify-center gap-2 text-sm text-muted-foreground"
      >
        <svg
          class="w-4 h-4 text-green-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
          />
        </svg>
        <span>安全加密连接</span>
      </div>
    </div>
  </div>
</template>
