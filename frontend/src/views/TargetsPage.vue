<template>
  <DashboardLayout>
    <div class="space-y-8">
      <!-- Page Header -->
      <div>
        <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
          <span>工作台</span>
          <span class="text-gray-600">›</span>
          <span class="text-primary">目标库</span>
        </div>
        <h1 class="text-3xl font-bold text-white mb-2">缺陷检测库</h1>
        <p class="text-gray-400">
          平台支持检测的所有钢材表面缺陷类别，点击任何缺陷可查看详细信息
        </p>
      </div>

      <!-- Search & Stats -->
      <div class="glass-card p-6">
        <!-- Search -->
        <div class="mb-6">
          <div class="relative max-w-md">
            <svg
              class="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2"
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
              v-model="searchQuery"
              type="text"
              placeholder="搜索缺陷类别或名称..."
              class="w-full pl-10 pr-4 py-2 bg-white/5 border border-primary/20 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 focus:bg-primary/5 transition-all"
            />
          </div>
        </div>

        <!-- Statistics -->
        <div
          class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-6 border-t border-primary/10"
        >
          <div class="p-4 bg-white/5 rounded-xl border border-primary/10">
            <div class="text-gray-400 text-xs mb-2">缺陷总数</div>
            <div class="text-3xl font-bold text-white">{{ totalDefects }}</div>
            <div class="text-primary text-xs mt-1">
              共 {{ allDefects.length }} 种
            </div>
          </div>
          <div
            class="p-4 bg-green-500/10 rounded-xl border border-green-500/20"
          >
            <div class="text-gray-400 text-xs mb-2">检测支持</div>
            <div class="text-3xl font-bold text-green-400">100%</div>
            <div class="text-green-400 text-xs mt-1">全部缺陷</div>
          </div>
          <div
            class="p-4 bg-orange-500/10 rounded-xl border border-orange-500/20"
          >
            <div class="text-gray-400 text-xs mb-2">高风险</div>
            <div class="text-3xl font-bold text-orange-400">
              {{ highRiskCount }}
            </div>
            <div class="text-orange-400 text-xs mt-1">需重点关注</div>
          </div>
          <div class="p-4 bg-cyan-500/10 rounded-xl border border-cyan-500/20">
            <div class="text-gray-400 text-xs mb-2">推荐模型</div>
            <div class="text-3xl font-bold text-cyan-400">
              {{ recommendedModelCount }}
            </div>
            <div class="text-cyan-400 text-xs mt-1">已配置</div>
          </div>
        </div>
      </div>

      <!-- Defects Selection Grid -->
      <div>
        <div class="flex items-center gap-2 mb-4">
          <div class="w-1 h-6 bg-primary rounded-full" />
          <h2 class="text-xl font-bold text-white">所有缺陷分类</h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <button
            v-for="defect in filteredDefects"
            :key="defect.id"
            @click="selectDefect(defect.id)"
            :class="[
              'p-4 rounded-xl transition-all duration-300 text-left group relative overflow-hidden',
              selectedDefectId === defect.id
                ? 'bg-primary/30 border-2 border-primary ring-2 ring-primary/50'
                : 'bg-white/5 border border-primary/20 hover:border-primary/50 hover:bg-white/10',
            ]"
          >
            <!-- Background glow effect for selected -->
            <div
              v-if="selectedDefectId === defect.id"
              class="absolute inset-0 bg-gradient-to-r from-primary/20 via-cyan-500/20 to-primary/20 opacity-50 group-hover:opacity-100 transition-opacity"
            />

              <div class="relative">
                <div class="flex items-center justify-between mb-2">
                  <h3 class="font-bold text-white text-base">{{ defect.name }}</h3>
                  <span class="text-xs px-2 py-1 rounded-full font-medium" :class="getRiskBadgeClass('')">
                    {{ defect.type || '缺陷类型' }}
                  </span>
                </div>
                <p class="text-xs text-gray-400 mb-3 truncate">
                  {{ defect.description || '暂无描述' }}
                </p>
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- Dynamic Detail Section -->
      <div v-if="selectedDefect" class="glass-card p-8">
        <div class="space-y-4">
          <h3 class="text-xl font-bold text-white">{{ selectedDefect.name }}</h3>
          <span class="px-3 py-1 rounded-full text-xs font-medium bg-primary/20 text-primary">{{ selectedDefect.type || '缺陷类型' }}</span>
          <p class="text-gray-300 text-sm leading-relaxed">{{ selectedDefect.description || '暂无描述' }}</p>
        </div>
      </div>

      <!-- Quick Reference Section (when no defect selected) -->
      <div v-else class="glass-card p-8">
        <div class="flex flex-col items-center justify-center py-16">
          <svg
            class="w-16 h-16 text-primary/40 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <h3 class="text-xl font-semibold text-white mb-2">
            选择一个缺陷查看详情
          </h3>
          <p class="text-gray-400 text-center max-w-2xl">
            从上方缺陷分类中选择任意一个缺陷类别，即可查看包括产生原因、风险影响、预防措施、示例图片、推荐检测模型等详细信息。
          </p>
        </div>
      </div>

      <!-- Detection Guide -->
      <div class="glass-card p-6">
        <h3 class="text-lg font-semibold text-white mb-4">检测指南</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex gap-4">
            <div
              class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm"
            >
              1
            </div>
            <div>
              <h4 class="font-medium text-white mb-1">上传高清图片</h4>
              <p class="text-sm text-gray-400">
                建议分辨率1920×1080以上，确保缺陷清晰可见
              </p>
            </div>
          </div>
          <div class="flex gap-4">
            <div
              class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm"
            >
              2
            </div>
            <div>
              <h4 class="font-medium text-white mb-1">选择合适模型</h4>
              <p class="text-sm text-gray-400">
                根据缺陷类型和精度要求选择对应的YOLO模型
              </p>
            </div>
          </div>
          <div class="flex gap-4">
            <div
              class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm"
            >
              3
            </div>
            <div>
              <h4 class="font-medium text-white mb-1">获取检测结果</h4>
              <p class="text-sm text-gray-400">
                毫秒级返回结果，显示所有检测到的缺陷位置和置信度
              </p>
            </div>
          </div>
          <div class="flex gap-4">
            <div
              class="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm"
            >
              4
            </div>
            <div>
              <h4 class="font-medium text-white mb-1">生成检测报告</h4>
              <p class="text-sm text-gray-400">
                自动生成详细报告，支持导出为PDF或Excel格式
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import DashboardLayout from "../layouts/DashboardLayout.vue";
import { getTargets } from "../api/targets";

const searchQuery = ref("");
const selectedDefectId = ref<string | null>(null);
const targets = ref<Array<{ id: string; name: string; type: string; description: string; image_url: string }>>([]);

onMounted(async () => {
  try {
    const res = await getTargets(1, 50)
    if (res.success) {
      targets.value = res.data.targets || []
    }
  } catch { /* silent */ }
})

// Get all defects
const allDefects = computed(() => targets.value);

// Get selected defect details
const selectedDefect = computed(() => {
  if (!selectedDefectId.value) return null;
  return targets.value.find(d => d.id === selectedDefectId.value) || null;
});

// Filter defects based on search query
const filteredDefects = computed(() => {
  if (!searchQuery.value) return allDefects.value
  const query = searchQuery.value.toLowerCase()
  return allDefects.value.filter(
    (defect) =>
      defect.name.toLowerCase().includes(query) ||
      (defect.type || '').toLowerCase().includes(query) ||
      (defect.description || '').toLowerCase().includes(query),
  )
})

const totalDefects = computed(() => allDefects.value.length)
const highRiskCount = computed(() => 0)
const recommendedModelCount = computed(() => 0)

const selectDefect = (defectId: string | null) => {
  selectedDefectId.value = selectedDefectId.value === defectId ? null : defectId
}

const getRiskBadgeClass = (_level: string) => 'bg-primary/20 text-primary'
</script>
