<template>
  <div class="min-h-screen bg-[#0a0e17] grid-pattern flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Particle Background -->
    <ParticleBackground />
    
    <!-- Decorative Elements -->
    <div class="absolute top-20 left-20 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl"></div>
    <div class="absolute bottom-20 right-20 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl"></div>
    
    <!-- Main Card -->
    <div class="glass-card p-8 w-full max-w-md relative z-10">
      <!-- Icon -->
      <div class="flex justify-center mb-6">
        <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 flex items-center justify-center">
          <svg class="w-10 h-10 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
      </div>
      
      <!-- Title -->
      <h2 class="text-2xl font-bold text-center text-white mb-2">找回密码</h2>
      <p class="text-gray-400 text-center mb-8">输入您的注册邮箱，我们将发送重置链接</p>
      
      <!-- Success Message -->
      <div v-if="emailSent" class="mb-6 p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
        <div class="flex items-center gap-3">
          <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-green-400 text-sm">重置链接已发送至您的邮箱，请查收</span>
        </div>
      </div>
      
      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Email Input -->
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <input
            v-model="email"
            type="email"
            placeholder="请输入注册邮箱"
            required
            class="w-full pl-12 pr-4 py-4 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-gray-500 focus:outline-none input-glow transition-all duration-300"
          />
        </div>
        
        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold rounded-xl btn-glow disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <svg v-if="isLoading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ isLoading ? '发送中...' : '发送重置链接' }}</span>
        </button>
      </form>
      
      <!-- Back to Login -->
      <div class="mt-6 text-center">
        <span class="text-gray-400">想起密码了？</span>
        <router-link to="/login" class="text-cyan-400 hover:text-cyan-300 ml-2 transition-colors">
          返回登录
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ParticleBackground from '../components/ParticleBackground.vue'

const email = ref('')
const isLoading = ref(false)
const emailSent = ref(false)

const handleSubmit = async () => {
  isLoading.value = true
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1500))
  emailSent.value = true
  isLoading.value = false
}
</script>
