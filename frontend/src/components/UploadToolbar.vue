<template>
  <div class="glass-card p-6 space-y-4">
    <div
      class="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-4"
    >
      <div>
        <h3 class="text-lg font-semibold text-white">批量检测控制</h3>
        <p class="text-gray-400 text-sm mt-1">
          支持多图上传、批量检测、导出结果与删除选中项。
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-3">
        <button
          @click="$emit('start')"
          :disabled="isBusy || !hasItems"
          class="btn-glow px-4 py-3 rounded-2xl bg-gradient-to-r from-primary to-cyan-400 text-white text-sm font-medium disabled:opacity-50"
        >
          {{ isBusy ? (isPaused ? "继续检测" : "检测中...") : "全部检测" }}
        </button>
        <button
          @click="$emit('pause')"
          :disabled="!isBusy"
          class="px-4 py-3 rounded-2xl border border-primary/20 text-sm text-primary hover:bg-white/5 transition-colors"
        >
          {{ isPaused ? "恢复检测" : "暂停检测" }}
        </button>
        <button
          @click="$emit('deleteSelected')"
          :disabled="!hasItems"
          class="px-4 py-3 rounded-2xl border border-red-500/20 text-sm text-red-300 hover:bg-red-500/10 transition-colors"
        >
          删除选中
        </button>
        <button
          @click="$emit('export')"
          :disabled="!hasItems"
          class="px-4 py-3 rounded-2xl border border-cyan-400/20 text-sm text-cyan-300 hover:bg-cyan-400/10 transition-colors"
        >
          导出结果
        </button>
      </div>
    </div>

    <div
      class="grid grid-cols-3 gap-4 pt-4 border-t border-primary/10 text-sm text-gray-400"
    >
      <div class="space-y-1">
        <div class="text-xs uppercase tracking-[0.12em] text-gray-500">
          上传数量
        </div>
        <div class="text-white font-semibold">
          {{ totalItems }} / {{ maxFiles }}
        </div>
      </div>
      <div class="space-y-1">
        <div class="text-xs uppercase tracking-[0.12em] text-gray-500">
          整体进度
        </div>
        <div class="text-white font-semibold">{{ progress }}%</div>
      </div>
      <div class="space-y-1">
        <div class="text-xs uppercase tracking-[0.12em] text-gray-500">
          当前状态
        </div>
        <div class="text-white font-semibold">{{ statusLabel }}</div>
      </div>
    </div>

    <div class="w-full h-2 rounded-full bg-white/5 overflow-hidden">
      <div
        class="h-full rounded-full bg-gradient-to-r from-primary to-cyan-400 transition-all duration-500"
        :style="{ width: progress + '%' }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
  totalItems: { type: Number, default: 0 },
  maxFiles: { type: Number, default: 10 },
  progress: { type: Number, default: 0 },
  isBusy: { type: Boolean, default: false },
  isPaused: { type: Boolean, default: false },
  hasItems: { type: Boolean, default: false },
});

const statusLabel = computed(() => {
  if (props.isBusy) {
    return props.isPaused ? "已暂停" : "检测中";
  }
  return props.hasItems ? "就绪" : "等待上传";
});
</script>
