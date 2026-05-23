<template>
  <DashboardLayout>
    <div class="space-y-6">
      <!-- Page Header -->
      <div>
        <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
          <span>工作台</span>
          <span class="text-gray-600">›</span>
          <span class="text-primary">目标库</span>
        </div>
        <h1 class="text-2xl font-bold text-white mb-2">缺陷检测库</h1>
        <p class="text-gray-400">平台支持检测的所有钢材表面缺陷类别</p>
      </div>

      <!-- Search & Stats -->
      <div class="glass-card p-6">
        <!-- Search -->
        <div class="mb-6">
          <div class="relative max-w-md">
            <svg class="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="搜索缺陷类别..." 
              class="w-full pl-10 pr-4 py-2 bg-white/5 border border-primary/20 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 focus:bg-primary/5 transition-all"
            />
          </div>
        </div>

        <!-- Statistics -->
        <div class="grid grid-cols-2 gap-4 pt-6 border-t border-primary/10">
          <div class="p-4 bg-white/5 rounded-xl border border-primary/10">
            <div class="text-gray-400 text-xs mb-2">缺陷总数</div>
            <div class="text-3xl font-bold text-white">{{ totalTargets }}</div>
            <div class="text-primary text-xs mt-1">共 {{ categories.length }} 类</div>
          </div>
          <div class="p-4 bg-green-500/10 rounded-xl border border-green-500/20">
            <div class="text-gray-400 text-xs mb-2">检测支持</div>
            <div class="text-3xl font-bold text-green-400">100%</div>
            <div class="text-green-400 text-xs mt-1">全部缺陷</div>
          </div>
        </div>
      </div>

      <!-- Categories Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div 
          v-for="category in filteredCategories" 
          :key="category.id"
          class="glass-card-hover p-6 group"
        >
          <!-- Category Header -->
          <div class="flex items-center gap-4 mb-5">
            <div :class="[
              'w-14 h-14 rounded-xl flex items-center justify-center transition-all group-hover:scale-110',
              category.colorBg
            ]">
              <component :is="category.icon" class="w-7 h-7" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">{{ category.name }}</h3>
              <p class="text-sm text-gray-400">{{ category.targets.length }} 个缺陷</p>
            </div>
          </div>
          
          <!-- Defects List -->
          <div class="space-y-2">
            <div 
              v-for="target in category.targets" 
              :key="target"
              class="flex items-center gap-3 p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-all border border-transparent hover:border-primary/30"
            >
              <svg class="w-4 h-4 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-white text-sm">{{ target }}</span>
            </div>
          </div>

          <!-- Category Badge -->
          <div class="mt-4 pt-4 border-t border-primary/10">
            <span :class="['badge-primary']">{{ category.type }}</span>
          </div>
        </div>
      </div>

      <!-- Detailed Defects Reference -->
      <div class="glass-card p-6">
        <div class="flex items-center gap-3 mb-6">
          <div class="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-white">缺陷详细说明</h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            v-for="defect in allDefects" 
            :key="defect.name"
            class="p-4 bg-white/5 rounded-xl hover:bg-white/10 border border-primary/10 hover:border-primary/30 transition-all cursor-pointer group"
          >
            <div class="font-semibold text-white group-hover:text-primary mb-2 transition-colors">{{ defect.name }}</div>
            <div class="text-xs text-gray-400 leading-relaxed">{{ defect.description }}</div>
            <div class="mt-3 flex items-center gap-1 text-primary text-xs opacity-0 group-hover:opacity-100 transition-opacity">
              <span>了解更多</span>
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Detection Guide -->
      <div class="glass-card p-6">
        <h3 class="text-lg font-semibold text-white mb-4">检测指南</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex gap-4">
            <div class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm">1</div>
            <div>
              <h4 class="font-medium text-white mb-1">上传高清图片</h4>
              <p class="text-sm text-gray-400">建议分辨率1920×1080以上，确保缺陷清晰可见</p>
            </div>
          </div>
          <div class="flex gap-4">
            <div class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm">2</div>
            <div>
              <h4 class="font-medium text-white mb-1">选择合适模型</h4>
              <p class="text-sm text-gray-400">yolo11n(快速)或yolo11m(精确)，根据场景选择</p>
            </div>
          </div>
          <div class="flex gap-4">
            <div class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm">3</div>
            <div>
              <h4 class="font-medium text-white mb-1">获取检测结果</h4>
              <p class="text-sm text-gray-400">毫秒级返回结果，显示所有检测到的缺陷位置</p>
            </div>
          </div>
          <div class="flex gap-4">
            <div class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm">4</div>
            <div>
              <h4 class="font-medium text-white mb-1">生成检测报告</h4>
              <p class="text-sm text-gray-400">自动生成详细报告，支持导出为PDF或Excel</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'

const searchQuery = ref('')

const categories = ref([
  {
    id: 1,
    name: '表面缺陷类',
    type: '高优先级',
    targets: ['裂纹', '斑点', '划痕'],
    colorBg: 'bg-red-500/20 text-red-400',
    icon: {
      render() {
        return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
          h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' })
        ])
      }
    }
  },
  {
    id: 2,
    name: '表面状态类',
    type: '中优先级',
    targets: ['麻面', '轧入氧化皮'],
    colorBg: 'bg-orange-500/20 text-orange-400',
    icon: {
      render() {
        return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
          h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
        ])
      }
    }
  },
  {
    id: 3,
    name: '内部缺陷类',
    type: '关键',
    targets: ['夹杂物'],
    colorBg: 'bg-cyan-500/20 text-cyan-400',
    icon: {
      render() {
        return h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
          h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
        ])
      }
    }
  }
])

const allDefects = [
  { name: '裂纹', description: '钢材表面的线性或分支状断裂痕迹，可能严重影响结构强度和安全性' },
  { name: '斑点', description: '表面出现的点状异常区域，通常由杂质、腐蚀或污染引起' },
  { name: '划痕', description: '表面的线性划伤痕迹，通常在运输、存储或加工过程中产生' },
  { name: '麻面', description: '表面呈现粗糙、凹凸不平的纹理状态，影响表面光洁度' },
  { name: '轧入氧化皮', description: '轧制过程中氧化皮被压入钢材表面形成的硬脆缺陷' },
  { name: '夹杂物', description: '钢材内部存在的非金属杂质，如硫化物、氧化物等，影响力学性能' }
]

const totalTargets = computed(() => {
  return categories.value.reduce((sum, cat) => sum + cat.targets.length, 0)
})

const filteredCategories = computed(() => {
  if (!searchQuery.value) return categories.value
  const query = searchQuery.value.toLowerCase()
  return categories.value.filter(cat => 
    cat.name.toLowerCase().includes(query) ||
    cat.targets.some(t => t.toLowerCase().includes(query))
  )
})
</script>

