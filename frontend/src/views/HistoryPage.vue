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
        <p class="text-gray-400">
          查看和管理您的所有检测任务，每个任务包含批量上传的完整检测结果
        </p>
      </div>

      <!-- Filters & Stats -->
      <div class="glass-card p-6">
        <div
          class="flex flex-col md:flex-row items-center gap-4 mb-6 pb-6 border-b border-primary/10"
        >
          <!-- Search -->
          <div class="relative flex-1">
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
              placeholder="搜索任务ID、任务名称..."
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
              <option value="completed" class="bg-gray-900">已完成</option>
              <option value="processing" class="bg-gray-900">进行中</option>
              <option value="failed" class="bg-gray-900">已失败</option>
            </select>

            <button
              @click="sortOrder = sortOrder === 'desc' ? 'asc' : 'desc'"
              class="px-4 py-2 bg-primary/20 border border-primary/30 rounded-xl text-sm text-primary hover:bg-primary/30 transition-all flex items-center gap-2"
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
                  d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
                />
              </svg>
              排序
            </button>
          </div>
        </div>

        <!-- Statistics -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="p-3 bg-white/5 rounded-xl border border-primary/10">
            <div class="text-gray-400 text-xs mb-1">总任务数</div>
            <div class="text-2xl font-bold text-white">{{ stats.total }}</div>
          </div>
          <div
            class="p-3 bg-green-500/10 rounded-xl border border-green-500/20"
          >
            <div class="text-gray-400 text-xs mb-1">已完成</div>
            <div class="text-2xl font-bold text-green-400">
              {{ stats.completed }}
            </div>
          </div>
          <div
            class="p-3 bg-yellow-500/10 rounded-xl border border-yellow-500/20"
          >
            <div class="text-gray-400 text-xs mb-1">进行中</div>
            <div class="text-2xl font-bold text-yellow-400">
              {{ stats.processing }}
            </div>
          </div>
          <div class="p-3 bg-red-500/10 rounded-xl border border-red-500/20">
            <div class="text-gray-400 text-xs mb-1">已失败</div>
            <div class="text-2xl font-bold text-red-400">
              {{ stats.failed }}
            </div>
          </div>
        </div>
      </div>

      <!-- Task History Table -->
      <div class="glass-card p-6 overflow-x-auto">
        <div v-if="filteredTasks.length === 0" class="text-center py-16">
          <div
            class="w-20 h-20 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center"
          >
            <svg
              class="w-10 h-10 text-primary"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <p class="text-white font-medium mb-1">暂无检测任务</p>
          <p class="text-gray-500 text-sm">进行批量上传后会自动生成检测任务</p>
        </div>

        <table v-else class="w-full text-sm">
          <thead>
            <tr class="border-b border-primary/10">
              <th class="text-left py-3 px-4 text-gray-400 font-medium">
                任务ID
              </th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">
                任务名称
              </th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">
                创建时间
              </th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">
                图片数
              </th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">
                缺陷数
              </th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">
                平均置信度
              </th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">
                状态
              </th>
              <th class="text-left py-3 px-4 text-gray-400 font-medium">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-primary/10">
            <tr
              v-for="task in filteredTasks"
              :key="task.id"
              class="hover:bg-white/5 transition-colors"
            >
              <td class="py-4 px-4">
                <span class="text-white font-medium font-mono text-xs">
                  {{ task.id.slice(-12) }}
                </span>
              </td>
              <td class="py-4 px-4">
                <span class="text-white font-medium">{{ task.taskName }}</span>
              </td>
              <td class="py-4 px-4 text-gray-400">
                {{ formatTime(task.createdAt) }}
              </td>
              <td class="py-4 px-4">
                <span class="text-white font-medium">{{
                  task.totalImages
                }}</span>
              </td>
              <td class="py-4 px-4">
                <span
                  :class="[
                    'text-white font-medium',
                    task.totalDefects > 10
                      ? 'text-orange-400'
                      : 'text-green-400',
                  ]"
                >
                  {{ task.totalDefects }}
                </span>
              </td>
              <td class="py-4 px-4">
                <span class="text-primary font-medium">
                  {{ (task.averageConfidence * 100).toFixed(1) }}%
                </span>
              </td>
              <td class="py-4 px-4">
                <div class="flex items-center gap-2">
                  <div
                    :class="[
                      'w-2 h-2 rounded-full',
                      task.status === 'completed'
                        ? 'bg-green-400'
                        : task.status === 'processing'
                          ? 'bg-yellow-400 animate-pulse'
                          : 'bg-red-400',
                    ]"
                  />
                  <span class="text-gray-300">
                    {{
                      task.status === "completed"
                        ? "已完成"
                        : task.status === "processing"
                          ? "进行中"
                          : "已失败"
                    }}
                  </span>
                </div>
              </td>
              <td class="py-4 px-4">
                <div class="flex items-center gap-2">
                  <button
                    @click="viewDetail(task)"
                    class="text-primary hover:text-cyan-400 transition-colors"
                    title="查看详情"
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
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                    </svg>
                  </button>
                  <button
                    @click="handleDelete(task.id)"
                    class="text-gray-400 hover:text-red-400 transition-colors"
                    title="删除任务"
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
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
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
          显示
          <span class="text-white font-medium">{{
            currentPage * pageSize - pageSize + 1
          }}</span>
          到
          <span class="text-white font-medium">{{
            Math.min(currentPage * pageSize, filteredTasks.length)
          }}</span>
          条，共
          <span class="text-white font-medium">{{ filteredTasks.length }}</span>
          条
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

    <!-- Task Detail Dialog -->
    <HistoryTaskDetail
      :is-open="isDetailOpen"
      :task="selectedTask!"
      @close="isDetailOpen = false"
    />
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import DashboardLayout from "../layouts/DashboardLayout.vue";
import HistoryTaskDetail from "../components/HistoryTaskDetail.vue";
import { useBatchDetectionStore } from "../stores/batchDetection";
import type { DetectionTask } from "../stores/batchDetection";

const store = useBatchDetectionStore();

const searchQuery = ref("");
const statusFilter = ref("");
const sortOrder = ref<"asc" | "desc">("desc");
const currentPage = ref(1);
const pageSize = 10;

const isDetailOpen = ref(false);
const selectedTask = ref<DetectionTask | null>(null);

const stats = computed(() => ({
  total: store.detectionTasks.length,
  completed: store.detectionTasks.filter((t) => t.status === "completed")
    .length,
  processing: store.detectionTasks.filter((t) => t.status === "processing")
    .length,
  failed: store.detectionTasks.filter((t) => t.status === "failed").length,
}));

const filteredTasks = computed(() => {
  let result = store.detectionTasks.filter((task) => {
    const matchSearch =
      task.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      task.taskName.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchStatus =
      !statusFilter.value || task.status === statusFilter.value;
    return matchSearch && matchStatus;
  });

  result.sort((a, b) => {
    const timeA = a.createdAt;
    const timeB = b.createdAt;
    return sortOrder.value === "desc" ? timeB - timeA : timeA - timeB;
  });

  return result;
});

const totalPages = computed(() =>
  Math.ceil(filteredTasks.value.length / pageSize),
);

const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleString("zh-CN");
};

const viewDetail = (task: DetectionTask) => {
  selectedTask.value = task;
  isDetailOpen.value = true;
};

const handleDelete = async (taskId: string) => {
  if (confirm("确定要删除这个任务吗？")) {
    store.detectionTasks = store.detectionTasks.filter((t) => t.id !== taskId);
    store.saveTasksToStorage();
  }
};

onMounted(() => {
  // Tasks are loaded from localStorage via store initialization
  store.loadTasksFromStorage();
});
</script>
