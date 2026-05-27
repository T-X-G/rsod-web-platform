<template>
  <div class="min-h-screen bg-[#0a0e17] flex relative overflow-hidden">
    <!-- Animated Background -->
    <div class="fixed inset-0 pointer-events-none">
      <!-- Grid Pattern -->
      <div
        class="absolute inset-0 bg-[linear-gradient(rgba(0,212,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,212,255,0.03)_1px,transparent_1px)] bg-[size:50px_50px]"
      ></div>
      <!-- Floating Orbs -->
      <div
        class="absolute top-20 left-20 w-96 h-96 bg-primary/5 rounded-full blur-3xl animate-pulse-slow"
      ></div>
      <div
        class="absolute bottom-20 right-20 w-80 h-80 bg-accent/5 rounded-full blur-3xl animate-pulse-slow"
        style="animation-delay: 1s"
      ></div>
    </div>

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed h-full z-30 transition-all duration-300 ease-out',
        sidebarExpanded ? 'w-56' : 'w-16',
      ]"
      @mouseenter="handleSidebarHover(true)"
      @mouseleave="handleSidebarHover(false)"
    >
      <!-- Sidebar Glow Effect -->
      <div
        :class="[
          'absolute inset-0 bg-gradient-to-r from-primary/20 to-transparent opacity-0 transition-opacity duration-300',
          sidebarHovered && !sidebarExpanded ? 'opacity-100' : '',
        ]"
      ></div>

      <!-- Sidebar Content -->
      <div
        class="relative h-full bg-[#0d1221]/90 backdrop-blur-xl border-r border-primary/20 flex flex-col"
      >
        <!-- Logo -->
        <div
          class="p-4 flex items-center gap-3 cursor-pointer border-b border-primary/10"
          @click="toggleSidebar"
        >
          <div
            class="w-10 h-10 min-w-[40px] bg-gradient-to-br from-primary to-cyan-400 rounded-xl flex items-center justify-center shadow-lg shadow-primary/30"
          >
            <svg
              class="w-6 h-6 text-white"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <rect
                x="3"
                y="3"
                width="18"
                height="18"
                rx="2"
                stroke-width="2"
              />
              <path
                d="M9 9h6M9 12h6M9 15h4"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </div>
          <transition name="fade-slide">
            <div
              v-if="sidebarExpanded"
              class="overflow-hidden whitespace-nowrap"
            >
              <div class="text-white font-bold text-sm">钢材缺陷检测</div>
              <div class="text-primary/70 text-xs">SteelDefect AI</div>
            </div>
          </transition>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 px-2 py-4 space-y-1">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            :class="[
              'group flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-300 relative',
              isActive(item.path)
                ? 'bg-primary/20 text-primary shadow-lg shadow-primary/10'
                : 'text-gray-400 hover:text-primary hover:bg-primary/10',
            ]"
          >
            <!-- Active Indicator -->
            <div
              v-if="isActive(item.path)"
              class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary rounded-r-full"
            ></div>

            <!-- Icon with Glow -->
            <div
              :class="[
                'relative min-w-[24px] transition-all duration-300',
                isActive(item.path)
                  ? 'text-primary'
                  : 'group-hover:text-primary',
              ]"
            >
              <component :is="item.icon" class="w-6 h-6" />
              <div
                :class="[
                  'absolute inset-0 blur-md transition-opacity duration-300',
                  isActive(item.path)
                    ? 'opacity-50 bg-primary'
                    : 'opacity-0 group-hover:opacity-30 group-hover:bg-primary',
                ]"
              ></div>
            </div>

            <transition name="fade-slide">
              <span
                v-if="sidebarExpanded"
                class="text-sm font-medium whitespace-nowrap"
                >{{ item.name }}</span
              >
            </transition>
          </router-link>
        </nav>

        <!-- Logout -->
        <div class="p-3 border-t border-primary/10">
          <button @click="handleLogout"
            class="w-full flex items-center justify-center gap-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-all py-2 rounded-lg text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <transition name="fade-slide">
              <span v-if="sidebarExpanded">退出</span>
            </transition>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div
      :class="[
        'flex-1 transition-all duration-300',
        sidebarExpanded ? 'ml-56' : 'ml-16',
      ]"
    >
      <!-- Top Header -->
      <header
        class="h-16 bg-[#0d1221]/80 backdrop-blur-xl border-b border-primary/10 flex items-center justify-between px-6 sticky top-0 z-20"
      >
        <!-- Left Side -->
        <div class="flex items-center gap-4">
          <!-- Breadcrumb -->
          <div class="flex items-center gap-2 text-sm">
            <router-link
              to="/dashboard"
              class="text-gray-500 hover:text-primary transition-colors"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                />
              </svg>
            </router-link>
            <span class="text-gray-600">/</span>
            <span class="text-white font-medium">{{ currentPageTitle }}</span>
          </div>
        </div>

        <!-- Right Side -->
        <div class="flex items-center gap-3">
          <!-- Search -->
          <div class="relative group">
            <svg
              class="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2 group-focus-within:text-primary transition-colors"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <input
              type="text"
              placeholder="搜索..."
              class="pl-10 pr-4 py-2 bg-white/5 border border-primary/20 rounded-xl text-sm w-48 text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 focus:bg-primary/5 transition-all"
            />
          </div>

          <!-- System Status -->
          <div
            class="flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/30 rounded-full text-green-400 text-sm"
          >
            <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            系统正常
          </div>

          <!-- Icons -->
          <button
            class="p-2 text-gray-400 hover:text-primary hover:bg-primary/10 rounded-xl transition-all"
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
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
              />
            </svg>
          </button>
          <button
            class="p-2 text-gray-400 hover:text-primary hover:bg-primary/10 rounded-xl transition-all relative"
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
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
              />
            </svg>
            <span
              class="absolute -top-0.5 -right-0.5 w-5 h-5 bg-accent text-white text-xs rounded-full flex items-center justify-center animate-pulse"
              >3</span
            >
          </button>
          <button
            class="p-2 text-gray-400 hover:text-primary hover:bg-primary/10 rounded-xl transition-all"
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
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
          </button>

          <!-- System Status -->
          <div
            class="flex items-center gap-3 pl-3 ml-2 border-l border-primary/20"
          >
            <div
              class="w-9 h-9 rounded-full ring-2 ring-primary/30 overflow-hidden"
            >
              <img
                src="https://api.dicebear.com/7.x/avataaars/svg?seed=Lily"
                alt="avatar"
                class="w-full h-full"
              />
            </div>
            <div class="text-sm hidden lg:block">
              <div class="font-medium text-white">Lily</div>
              <div class="text-gray-500 text-xs">普通用户</div>
            </div>
            <svg
              class="w-4 h-4 text-gray-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="p-6 relative z-10">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

// Sidebar state
const sidebarExpanded = ref(false);
const sidebarHovered = ref(false);
const sidebarLocked = ref(false);

const handleSidebarHover = (isHovered: boolean) => {
  sidebarHovered.value = isHovered;
};

const toggleSidebar = () => {
  sidebarExpanded.value = !sidebarExpanded.value;
  sidebarLocked.value = sidebarExpanded.value;
};

// Navigation Items
const navItems = [
  {
    name: "智能检测",
    path: "/dashboard/detection",
    icon: {
      render() {
        return h(
          "svg",
          { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
          [
            h("path", {
              "stroke-linecap": "round",
              "stroke-linejoin": "round",
              "stroke-width": "2",
              d: "M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z",
            }),
          ],
        );
      },
    },
  },
  {
    name: "历史记录",
    path: "/dashboard/history",
    icon: {
      render() {
        return h(
          "svg",
          { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
          [
            h("path", {
              "stroke-linecap": "round",
              "stroke-linejoin": "round",
              "stroke-width": "2",
              d: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
            }),
          ],
        );
      },
    },
  },
  {
    name: "AI 问答",
    path: "/dashboard/ai-chat",
    icon: {
      render() {
        return h(
          "svg",
          { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
          [
            h("path", {
              "stroke-linecap": "round",
              "stroke-linejoin": "round",
              "stroke-width": "2",
              d: "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z",
            }),
          ],
        );
      },
    },
  },
  {
    name: "目标库",
    path: "/dashboard/targets",
    icon: {
      render() {
        return h(
          "svg",
          { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
          [
            h("path", {
              "stroke-linecap": "round",
              "stroke-linejoin": "round",
              "stroke-width": "2",
              d: "M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10",
            }),
          ],
        );
      },
    },
  },
  {
    name: "摄像头检测",
    path: "/dashboard/camera",
    icon: {
      render() {
        return h(
          "svg",
          { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
          [
            h("path", {
              "stroke-linecap": "round",
              "stroke-linejoin": "round",
              "stroke-width": "2",
              d: "M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z",
            }),
          ],
        );
      },
    },
  },
  {
    name: "视频检测",
    path: "/dashboard/video-detection",
    icon: {
      render() {
        return h("svg", { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" }, [
          h("path", { "stroke-linecap": "round", "stroke-linejoin": "round", "stroke-width": "2", d: "M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" }),
        ]);
      },
    },
  },
  {
    name: "个人中心",
    path: "/dashboard/profile",
    icon: {
      render() {
        return h(
          "svg",
          { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
          [
            h("path", {
              "stroke-linecap": "round",
              "stroke-linejoin": "round",
              "stroke-width": "2",
              d: "M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z",
            }),
          ],
        );
      },
    },
  },
];

const isActive = (path: string) => {
  return route.path === path || route.path.startsWith(path + "/");
};

const currentPageTitle = computed(() => {
  const item = navItems.find((item) => isActive(item.path));
  return item?.name || "工作台";
});

const handleLogout = () => {
  localStorage.removeItem("token");
  router.push("/login");
};
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes pulse-slow {
  0%,
  100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}
</style>
