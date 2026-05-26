<template>
  <DashboardLayout>
    <div class="space-y-6">
      <!-- User Profile Banner -->
      <div class="glass-card p-8">
        <div class="flex items-center gap-8">
          <!-- Avatar -->
          <div class="w-24 h-24 min-w-[96px] rounded-2xl bg-gradient-to-br from-primary to-cyan-400 p-1 shadow-lg shadow-primary/30">
            <div class="w-full h-full rounded-2xl overflow-hidden bg-[#0d1221] flex items-center justify-center">
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Lily" alt="avatar" class="w-full h-full" />
            </div>
          </div>

          <!-- User Info -->
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <h1 class="text-3xl font-bold text-white">{{ user.username || '用户' }}</h1>
              <span class="px-3 py-1 bg-primary/20 border border-primary/30 rounded-full text-primary text-sm font-medium">{{ user.role === 'admin' ? '管理员' : '普通用户' }}</span>
            </div>
            <p class="text-gray-400 mb-3">普通用户 · 注册于 2024-01-15 · 已使用 12 天</p>
            <div class="flex items-center gap-4 text-sm">
              <span class="flex items-center gap-1 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                user@example.com
              </span>
              <span class="flex items-center gap-1 text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                最后登录：2024-05-20 14:30
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-3">
            <button class="px-6 py-2 bg-primary/20 border border-primary/30 text-primary rounded-lg hover:bg-primary/30 transition-all">
              编辑资料
            </button>
            <button class="px-6 py-2 bg-gradient-to-r from-primary to-cyan-400 text-white rounded-lg hover:shadow-lg hover:shadow-primary/30 transition-all">
              升级会员
            </button>
          </div>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- Total Detections -->
        <div class="glass-card p-5">
          <div class="flex items-center justify-between mb-3">
            <span class="text-sm text-gray-400">总检测次数</span>
            <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
            </svg>
          </div>
          <div class="flex items-baseline gap-2 mb-3">
            <span class="text-3xl font-bold text-white">128</span>
            <span class="text-sm text-green-400 font-medium">+12%</span>
          </div>
          <div class="flex gap-1">
            <div v-for="i in 6" :key="i" :class="['flex-1 h-2 rounded-full', i === 6 ? 'bg-primary' : 'bg-primary/20']"></div>
          </div>
        </div>

        <!-- Total Targets -->
        <div class="glass-card p-5">
          <div class="flex items-center justify-between mb-3">
            <span class="text-sm text-gray-400">累计检测目标</span>
            <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
            </svg>
          </div>
          <div class="flex items-baseline gap-2 mb-3">
            <span class="text-3xl font-bold text-white">892</span>
            <span class="text-sm text-green-400 font-medium">+8%</span>
          </div>
          <div class="flex gap-1">
            <div v-for="i in 6" :key="i" :class="['flex-1 h-2 rounded-full', i === 6 ? 'bg-primary' : 'bg-primary/20']"></div>
          </div>
        </div>

        <!-- Success Rate -->
        <div class="glass-card p-5">
          <div class="flex items-center justify-between mb-3">
            <span class="text-sm text-gray-400">检测成功率</span>
            <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="flex items-baseline gap-2 mb-3">
            <span class="text-3xl font-bold text-white">98.5%</span>
            <span class="text-sm text-green-400 font-medium">+2.3%</span>
          </div>
          <div class="h-2 bg-white/5 rounded-full overflow-hidden border border-green-500/20">
            <div class="h-full bg-gradient-to-r from-green-400 to-green-500 rounded-full" style="width: 98.5%"></div>
          </div>
        </div>

        <!-- Avg Detection Time -->
        <div class="glass-card p-5">
          <div class="flex items-center justify-between mb-3">
            <span class="text-sm text-gray-400">平均检测时长</span>
            <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </div>
          <div class="flex items-baseline gap-2 mb-3">
            <span class="text-3xl font-bold text-white">156ms</span>
            <span class="text-sm text-green-400 font-medium">-0.5s</span>
          </div>
          <div class="flex gap-1">
            <div v-for="i in 6" :key="i" :class="['flex-1 h-2 rounded-full', i === 6 ? 'bg-primary' : 'bg-primary/20']"></div>
          </div>
        </div>
      </div>

      <!-- Account & Settings -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Account Info -->
        <div class="glass-card p-6">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
              <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white">账户信息</h3>
          </div>

          <div class="space-y-1">
            <div class="flex items-center justify-between py-4 px-0 border-b border-primary/10 hover:bg-white/5 px-3 py-3 rounded transition-colors">
              <span class="text-gray-400">用户名</span>
              <span class="text-white font-medium font-mono">example_user</span>
            </div>
            <div class="flex items-center justify-between py-4 px-0 border-b border-primary/10 hover:bg-white/5 px-3 py-3 rounded transition-colors">
              <span class="text-gray-400">邮箱地址</span>
              <span class="text-white font-medium">user@example.com</span>
            </div>
            <div class="flex items-center justify-between py-4 px-0 border-b border-primary/10 hover:bg-white/5 px-3 py-3 rounded transition-colors">
              <span class="text-gray-400">账户类型</span>
              <span class="text-primary font-medium">VIP 高级用户</span>
            </div>
            <div class="flex items-center justify-between py-4 px-0 hover:bg-white/5 px-3 py-3 rounded transition-colors">
              <span class="text-gray-400">注册时间</span>
              <span class="text-white font-medium">2024-01-15</span>
            </div>
          </div>
        </div>

        <!-- Preferences -->
        <div class="glass-card p-6">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
              <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white">偏好设置</h3>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-primary/10">
              <div>
                <div class="text-white font-medium">自动检测</div>
                <div class="text-xs text-gray-400 mt-0.5">上传后自动开始检测</div>
              </div>
              <button 
                @click="settings.autoDetect = !settings.autoDetect"
                :class="[
                  'relative w-12 h-6 rounded-full transition-all',
                  settings.autoDetect ? 'bg-primary' : 'bg-white/10 border border-primary/20'
                ]"
              >
                <div :class="[
                  'absolute top-1 w-4 h-4 bg-white rounded-full transition-transform',
                  settings.autoDetect ? 'translate-x-7' : 'translate-x-1'
                ]"></div>
              </button>
            </div>

            <div class="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-primary/10">
              <div>
                <div class="text-white font-medium">通知提醒</div>
                <div class="text-xs text-gray-400 mt-0.5">接收检测完成通知</div>
              </div>
              <button 
                @click="settings.notifications = !settings.notifications"
                :class="[
                  'relative w-12 h-6 rounded-full transition-all',
                  settings.notifications ? 'bg-primary' : 'bg-white/10 border border-primary/20'
                ]"
              >
                <div :class="[
                  'absolute top-1 w-4 h-4 bg-white rounded-full transition-transform',
                  settings.notifications ? 'translate-x-7' : 'translate-x-1'
                ]"></div>
              </button>
            </div>

            <div class="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-primary/10">
              <div>
                <div class="text-white font-medium">邮件通知</div>
                <div class="text-xs text-gray-400 mt-0.5">重要信息通过邮件通知</div>
              </div>
              <button 
                @click="settings.emailNotif = !settings.emailNotif"
                :class="[
                  'relative w-12 h-6 rounded-full transition-all',
                  settings.emailNotif ? 'bg-primary' : 'bg-white/10 border border-primary/20'
                ]"
              >
                <div :class="[
                  'absolute top-1 w-4 h-4 bg-white rounded-full transition-transform',
                  settings.emailNotif ? 'translate-x-7' : 'translate-x-1'
                ]"></div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-3">
        <button class="px-6 py-3 bg-gradient-to-r from-primary to-cyan-400 text-white rounded-xl font-medium hover:shadow-lg hover:shadow-primary/30 transition-all flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          保存设置
        </button>
        <button class="px-6 py-3 border border-primary/30 text-primary rounded-xl font-medium hover:bg-primary/10 transition-all flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
          </svg>
          修改密码
        </button>
        <button @click="handleLogout" class="px-6 py-3 border border-red-500/20 text-red-400 rounded-xl font-medium hover:bg-red-500/10 transition-all ml-auto flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span>退出登录</span>
        </button>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { getMe } from '../api/auth'

const router = useRouter()
const user = ref<{ username?: string; email?: string; role?: string; id?: string }>({})

onMounted(async () => {
  try {
    const res = await getMe()
    if (res.success) {
      user.value = res.data
    }
  } catch { /* silent */ }
})

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const settings = ref({
  autoDetect: true,
  notifications: true,
  emailNotif: false
})
</script>

