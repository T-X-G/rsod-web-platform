<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ParticleBackground from '../components/ParticleBackground.vue'
import LogoIcon from '../components/LogoIcon.vue'

const router = useRouter()
const isVisible = ref(false)

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 100)
})

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const features = [
  {
    icon: 'scan',
    title: '高精度检测',
    desc: '基于YOLOv11深度学习模型，检测精度达99.2%'
  },
  {
    icon: 'speed',
    title: '实时处理',
    desc: '毫秒级响应，支持生产线实时检测需求'
  },
  {
    icon: 'chart',
    title: '智能分析',
    desc: '自动分类缺陷类型，生成详细检测报告'
  }
]
</script>

<template>
  <div class="min-h-screen bg-background relative overflow-hidden">
    <!-- Background Effects -->
    <ParticleBackground />
    <div class="absolute inset-0 grid-pattern opacity-50"></div>
    
    <!-- Gradient Orbs -->
    <div class="absolute top-20 left-10 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl animate-float"></div>
    <div class="absolute bottom-20 right-10 w-80 h-80 bg-accent/10 rounded-full blur-3xl animate-float" style="animation-delay: -3s;"></div>
    
    <!-- Content -->
    <div class="relative z-10 min-h-screen flex flex-col">
      <!-- Header -->
      <header class="px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <LogoIcon class="w-10 h-10" />
          <span class="text-xl font-bold text-foreground">SteelVision</span>
        </div>
        <nav class="hidden md:flex items-center gap-6">
          <a href="#features" class="text-muted-foreground hover:text-primary transition-colors">功能特性</a>
          <a href="#about" class="text-muted-foreground hover:text-primary transition-colors">关于我们</a>
        </nav>
      </header>

      <!-- Hero Section -->
      <main class="flex-1 flex items-center justify-center px-6 py-12">
        <div 
          class="max-w-6xl w-full grid lg:grid-cols-2 gap-12 items-center"
          :class="{ 'opacity-0 translate-y-8': !isVisible, 'opacity-100 translate-y-0': isVisible }"
          style="transition: all 0.8s ease-out;"
        >
          <!-- Left: Text Content -->
          <div class="text-center lg:text-left space-y-8">
            <div class="space-y-4">
              <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
                <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                <span class="text-sm text-primary">AI驱动的工业检测解决方案</span>
              </div>
              
              <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
                <span class="text-foreground">钢铁表面缺陷</span>
                <br />
                <span class="gradient-text">智能检测平台</span>
              </h1>
              
              <p class="text-lg text-muted-foreground max-w-xl mx-auto lg:mx-0 leading-relaxed">
                融合YOLOv11深度学习技术，为钢铁制造业提供高精度、实时化的表面缺陷检测解决方案，助力智能制造升级
              </p>
            </div>

            <!-- CTA Buttons -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button
                @click="goToLogin"
                class="btn-glow px-8 py-4 bg-primary text-primary-foreground font-semibold rounded-xl shadow-glow hover:shadow-glow-lg transition-all duration-300"
              >
                <span class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                  登录系统
                </span>
              </button>
              
              <button
                @click="goToRegister"
                class="px-8 py-4 bg-transparent border-2 border-primary/50 text-primary font-semibold rounded-xl hover:bg-primary/10 hover:border-primary transition-all duration-300"
              >
                <span class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                  注册账号
                </span>
              </button>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-3 gap-6 pt-8 border-t border-border">
              <div class="text-center lg:text-left">
                <div class="text-3xl font-bold text-primary">99.2%</div>
                <div class="text-sm text-muted-foreground">检测精度</div>
              </div>
              <div class="text-center lg:text-left">
                <div class="text-3xl font-bold text-primary">50ms</div>
                <div class="text-sm text-muted-foreground">响应速度</div>
              </div>
              <div class="text-center lg:text-left">
                <div class="text-3xl font-bold text-primary">24/7</div>
                <div class="text-sm text-muted-foreground">全天候监测</div>
              </div>
            </div>
          </div>

          <!-- Right: Visual Element -->
          <div class="relative flex items-center justify-center">
            <div class="relative w-full max-w-md aspect-square">
              <!-- Outer Ring -->
              <div class="absolute inset-0 rounded-full border-2 border-primary/20 animate-pulse"></div>
              <div class="absolute inset-4 rounded-full border border-primary/30"></div>
              <div class="absolute inset-8 rounded-full border border-primary/40"></div>
              
              <!-- Center Card -->
              <div class="absolute inset-12 glass-card rounded-2xl flex flex-col items-center justify-center p-6 shadow-card">
                <!-- Scanner Animation -->
                <div class="relative w-full h-32 bg-muted rounded-lg overflow-hidden mb-4">
                  <div class="absolute inset-0 flex items-center justify-center">
                    <svg class="w-20 h-20 text-primary/30" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                  </div>
                  <div class="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-primary to-transparent scanner-line"></div>
                </div>
                
                <div class="text-center">
                  <div class="text-sm text-muted-foreground mb-1">检测状态</div>
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                    <span class="text-foreground font-medium">系统就绪</span>
                  </div>
                </div>
              </div>
              
              <!-- Floating Elements -->
              <div class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-4 px-3 py-1.5 glass-card rounded-full text-xs text-primary flex items-center gap-1.5">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
                缺陷识别
              </div>
              
              <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-4 px-3 py-1.5 glass-card rounded-full text-xs text-accent flex items-center gap-1.5">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M13 2.05v2.02c3.95.49 7 3.85 7 7.93 0 3.21-1.92 6-4.72 7.28L13 17v5l5-5-2.28-2.28C18.94 13.12 20 10.68 20 8c0-5.18-3.95-9.45-9-9.95zM11 2.05C5.94 2.55 2 6.81 2 12c0 2.68 1.06 5.11 2.77 6.9L2.5 21.17 3.91 22.59 6.18 20.32C7.97 21.4 10.09 22 12.25 22c.74 0 1.47-.07 2.18-.19L12 19.39c-.33.07-.67.11-1.02.11-3.87 0-7-3.13-7-7 0-4.08 3.05-7.44 7-7.93V2.05z"/>
                </svg>
                实时分析
              </div>
              
              <div class="absolute top-1/2 left-0 -translate-y-1/2 -translate-x-4 px-3 py-1.5 glass-card rounded-full text-xs text-secondary flex items-center gap-1.5 animate-float" style="animation-delay: -2s;">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                </svg>
                数据报表
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- Features Section -->
      <section id="features" class="px-6 py-16">
        <div class="max-w-6xl mx-auto">
          <h2 class="text-3xl font-bold text-center mb-12">
            <span class="gradient-text">核心功能</span>
          </h2>
          
          <div class="grid md:grid-cols-3 gap-6">
            <div 
              v-for="(feature, index) in features" 
              :key="index"
              class="glass-card p-6 rounded-2xl hover:border-primary/40 transition-all duration-300 group"
            >
              <div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                <svg v-if="feature.icon === 'scan'" class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <svg v-if="feature.icon === 'speed'" class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <svg v-if="feature.icon === 'chart'" class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-foreground mb-2">{{ feature.title }}</h3>
              <p class="text-muted-foreground leading-relaxed">{{ feature.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="px-6 py-8 border-t border-border">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-2">
            <LogoIcon class="w-6 h-6" />
            <span class="text-muted-foreground">© 2024 SteelVision. All rights reserved.</span>
          </div>
          <div class="flex items-center gap-4 text-sm text-muted-foreground">
            <span>技术支持: YOLOv11 + FastAPI</span>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>
