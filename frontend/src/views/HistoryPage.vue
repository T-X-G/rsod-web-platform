<template>
  <DashboardLayout>
    <div class="space-y-6">
      <!-- Page Header -->
      <div>
        <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
          <span>工作台</span>
          <span class="text-gray-600">›</span>
          <span class="text-primary">历史记录</span>
        </div>
        <h1 class="text-2xl font-bold text-white mb-2">检测历史记录</h1>
        <p class="text-gray-400">查看和管理您的所有检测记录，可按状态、类型等进行筛选</p>
      </div>

      <!-- Filters & Stats -->
      <div class="glass-card p-6">
        <div class="flex flex-col md:flex-row items-center gap-4 mb-6 pb-6 border-b border-primary/10">
          <!-- Search -->
          <div class="relative flex-1">
            <svg class="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="搜索检测ID、文件名..." 
              class="w-full pl-10 pr-4 py-2 bg-white/5 border border-primary/20 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary/50 focus:bg-primary/5 transition-all"
            />
          </div>

          <!-- Filters -->
          <div class="flex flex-wrap gap-3">
            <select 
              v-model="statusFilter"
              class="px-4 py-2 bg-white/5 border border-primary/20 rounded-xl text-sm text-white focus:outline-none focus:border-primary/50 transition-all"
            >
              <option value="" class="bg-gray-900">全部状态</option>
              <option value="completed" class="bg-gray-900">检测完成</option>
              <option value="processing" class="bg-gray-900">检测中</option>
              <option value="failed" class="bg-gray-900">检测失败</option>
            </select>

            <select 
              v-model="typeFilter"
              class="px-4 py-2 bg-white/5 border border-primary/20 rounded-xl text-sm text-white focus:outline-none focus:border-primary/50 transition-all"
            >
              <option value="" class="bg-gray-900">全部类型</option>
              <option value="single" class="bg-gray-900">单图检测</option>
              <option value="batch" class="bg-gray-900">批量检测</option>
            </select>

            <button 
              @click="sortOrder = sortOrder === 'desc' ? 'asc' : 'desc'"
              class="px-4 py-2 bg-primary/20 border border-primary/30 rounded-xl text-sm text-primary hover:bg-primary/30 transition-all flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              排序
            </button>
          </div>
        </div>

        <!-- Statistics -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="p-3 bg-white/5 rounded-xl border border-primary/10">
            <div class="text-gray-400 text-xs mb-1">总检测次数</div>
            <div class="text-2xl font-bold text-white">{{ stats.total }}</div>
            <div class="text-primary text-xs mt-1">+{{ stats.totalTrend }}%</div>
          </div>
          <div class="p-3 bg-green-500/10 rounded-xl border border-green-500/20">
            <div class="text-gray-400 text-xs mb-1">检测成功</div>
            <div class="text-2xl font-bold text-green-400">{{ stats.completed }}</div>
            <div class="text-green-400 text-xs mt-1">+{{ stats.completedTrend }}%</div>
          </div>
          <div class="p-3 bg-yellow-500/10 rounded-xl border border-yellow-500/20">
            <div class="text-gray-400 text-xs mb-1">检测中</div>
            <div class="text-2xl font-bold text-yellow-400">{{ stats.processing }}</div>
          </div>
          <div class="p-3 bg-red-500/10 rounded-xl border border-red-500/20">
            <div class="text-gray-400 text-xs mb-1">检测失败</div>
            <div class="text-2xl font-bold text-red-400">{{ stats.failed }}</div>
          </div>
        </div>
      </div>

      <!-- History Table -->
      <div class="glass-card p-6 overflow-x-auto">
        <div v-if="filteredHistory.length === 0" class="text-center py-16">
          <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center">
            <svg class="w-10 h-10 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-white font-medium mb-1">暂无检测记录</p>
          <p class="text-gray-500 text-sm">开始上传图片进行检测</p>
        </div>

        <table v-else class="w-full text-sm">
          <thead>
            <tr class="border-b border-primary/10">
              <th class="text-left py-3 px-4 text-gray-400 font-medium">检测ID</th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">检测类型</th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">检测时间</th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">缺陷数</th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">状态</th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-primary/10">
            <tr 
              v-for="item in filteredHistory" 
              :key="item.id"
              class="hover:bg-white/5 transition-colors"
            >
              <td class="py-4 px-4">
                <span class="text-white font-medium font-mono">{{ item.id }}</span>
              </td>
              <td class="py-4 px-4">
                <span class="px-3 py-1 rounded-full text-xs font-medium bg-primary/20 text-primary">
                  检测记录
                </span>
              </td>
                <td class="py-4 px-4 text-gray-400">{{ formatTime(item.created_at) }}</td>
              <td class="py-4 px-4">
                <span :class="['text-white font-medium', item.total_objects > 5 ? 'text-red-400' : 'text-green-400']">
                  {{ item.total_objects }}
                </span>
              </td>
              <td class="py-4 px-4">
                <div class="flex items-center gap-2">
                  <div 
                    :class="[
                      'w-2 h-2 rounded-full',
                      item.status === 'completed' ? 'bg-green-400' : 
                      item.status === 'processing' ? 'bg-yellow-400 animate-pulse' : 
                      'bg-red-400'
                    ]"
                  ></div>
                  <span class="text-gray-300">
                    {{ item.status === 'completed' ? '完成' : item.status === 'processing' ? '进行中' : '失败' }}
                  </span>
                </div>
              </td>
              <td class="py-4 px-4">
                <div class="flex items-center gap-2">
                  <button 
                    @click="viewDetail(item.id)"
                    class="text-primary hover:text-cyan-400 transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button 
                    @click="downloadReport(item.id)"
                    class="text-gray-400 hover:text-primary transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </button>
                  <button 
                    @click="handleDelete(item.id)"
                    class="text-gray-400 hover:text-red-400 transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-between">
        <div class="text-gray-400 text-sm">
          显示 <span class="text-white font-medium">{{ currentPage * pageSize - pageSize + 1 }}</span> 到 
          <span class="text-white font-medium">{{ Math.min(currentPage * pageSize, filteredHistory.length) }}</span> 
          条，共 <span class="text-white font-medium">{{ filteredHistory.length }}</span> 条
        </div>
        <div class="flex items-center gap-2">
          <button 
            @click="currentPage > 1 && currentPage--"
            :disabled="currentPage === 1"
            class="px-3 py-2 bg-primary/20 border border-primary/30 rounded-lg text-primary disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/30 transition-all"
          >
            上一页
          </button>
          <span class="text-gray-400 text-sm">第 {{ currentPage }} 页</span>
          <button 
            @click="currentPage < totalPages && currentPage++"
            :disabled="currentPage >= totalPages"
            class="px-3 py-2 bg-primary/20 border border-primary/30 rounded-lg text-primary disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/30 transition-all"
          >
            下一页
          </button>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { getHistory, deleteRecord as deleteRecordApi } from '../api/detection'

const searchQuery = ref('')
const statusFilter = ref('')
const typeFilter = ref('')
const sortOrder = ref<'asc' | 'desc'>('desc')
const currentPage = ref(1)
const pageSize = 10

const stats = ref({
  total: 0, totalTrend: 0, completed: 0, completedTrend: 0, processing: 0, failed: 0
})

const historyData = ref<Array<{
  id: string; filename: string; total_objects: number; detection_time: number;
  result_image_url: string; created_at: string; status: string;
}>>([])

onMounted(async () => {
  try {
    const res = await getHistory(1, 50)
    if (res.success) {
      historyData.value = res.data?.records || []
      stats.value.total = res.data?.total || historyData.value.length
    }
  } catch { console.error('operation failed') }
})

const filteredHistory = computed(() => {
  let result = historyData.value.filter(item => {
    const matchSearch = item.id.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchStatus = !statusFilter.value || item.status === statusFilter.value
    return matchSearch && matchStatus
  })
  result.sort((a, b) => {
    const timeA = new Date(a.created_at).getTime()
    const timeB = new Date(b.created_at).getTime()
    return sortOrder.value === 'desc' ? timeB - timeA : timeA - timeB
  })
  return result
})

const totalPages = computed(() => Math.ceil(filteredHistory.value.length / pageSize))

const formatTime = (t: string) => {
  if (!t) return ''
  return new Date(t).toLocaleString('zh-CN')
}

const viewDetail = (id: string) => { console.log('查看详情:', id) }
const downloadReport = (id: string) => { console.log('下载报告:', id) }

const handleDelete = async (id: string) => {
  try {
    await deleteRecordApi(id)
    historyData.value = historyData.value.filter(item => item.id !== id)
  } catch { console.error('operation failed') }
}
</script>

