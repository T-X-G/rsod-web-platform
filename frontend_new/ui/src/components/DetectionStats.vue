<template>
  <div class="glass-card p-6 space-y-4">
    <div class="flex items-center gap-3 mb-4">
      <div
        class="w-12 h-12 rounded-3xl bg-primary/10 flex items-center justify-center text-primary"
      >
        <svg
          class="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 17v-3a2 2 0 012-2h2a2 2 0 012 2v3m-6 0h6m-3-6v-4m-2 2h4"
          />
        </svg>
      </div>
      <div>
        <h3 class="text-lg font-semibold text-white">检测统计</h3>
        <p class="text-gray-400 text-sm">当前批次检测概览与缺陷分布</p>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4 text-sm">
      <div class="p-4 bg-white/5 rounded-3xl border border-primary/10">
        <div class="text-gray-400">图像总数</div>
        <div class="text-white text-2xl font-semibold">{{ totalImages }}</div>
      </div>
      <div class="p-4 bg-white/5 rounded-3xl border border-primary/10">
        <div class="text-gray-400">缺陷总数</div>
        <div class="text-white text-2xl font-semibold">{{ totalDefects }}</div>
      </div>
      <div class="p-4 bg-white/5 rounded-3xl border border-primary/10">
        <div class="text-gray-400">平均置信度</div>
        <div class="text-white text-2xl font-semibold">
          {{ (averageConfidence * 100).toFixed(1) }}%
        </div>
      </div>
      <div class="p-4 bg-white/5 rounded-3xl border border-primary/10">
        <div class="text-gray-400">完成数</div>
        <div class="text-white text-2xl font-semibold">
          {{ completedCount }}
        </div>
      </div>
    </div>

    <div class="space-y-3 pt-4 border-t border-primary/10">
      <div
        class="flex items-center justify-between text-xs uppercase tracking-[0.2em] text-gray-500"
      >
        <span>缺陷类别分布</span>
        <span class="text-white">共 {{ categorySummary.length }} 类</span>
      </div>
      <div class="space-y-3">
        <div
          v-for="item in categorySummary"
          :key="item.label"
          class="flex items-center justify-between gap-4"
        >
          <div class="min-w-[110px] text-sm text-gray-300">
            {{ item.label }}
          </div>
          <div class="flex-1 h-2 rounded-full bg-white/5 overflow-hidden">
            <div
              class="h-full rounded-full bg-gradient-to-r from-primary to-cyan-400"
              :style="{ width: getCategoryRatio(item) + '%' }"
            ></div>
          </div>
          <div class="text-xs text-gray-400">{{ item.count }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  totalImages: { type: Number, default: 0 },
  totalDefects: { type: Number, default: 0 },
  averageConfidence: { type: Number, default: 0 },
  completedCount: { type: Number, default: 0 },
  categorySummary: {
    type: Array as () => { label: string; count: number }[],
    default: () => [],
  },
});

const getCategoryRatio = (item: { label: string; count: number }) => {
  if (!props.totalDefects) return 0;
  return Math.min(100, Math.round((item.count / props.totalDefects) * 100));
};
</script>
