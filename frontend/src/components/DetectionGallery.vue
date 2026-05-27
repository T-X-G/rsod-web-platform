<template>
  <div class="glass-card p-6 space-y-4">
    <div class="flex items-center justify-between gap-4 mb-4">
      <div>
        <h3 class="text-lg font-semibold text-white">检测结果预览</h3>
        <p class="text-gray-400 text-sm">
          漏检率、类别标签和置信度全部可视化。
        </p>
      </div>
      <div class="text-xs text-gray-400">支持结果联动与缩略图切换</div>
    </div>

    <div class="space-y-4">
      <div v-if="currentItem" class="relative">
        <ImageViewer
          :src="currentItem.resultImage"
          :alt="currentItem.fileName"
        />
        <div
          class="absolute left-4 top-4 rounded-full bg-black/40 px-3 py-1 text-xs text-cyan-100 backdrop-blur-sm shadow-[0_0_20px_rgba(0,212,255,0.15)]"
        >
          {{ currentItem.detections.length }} 处缺陷
        </div>
        <div
          v-if="currentItem.detections.length"
          class="absolute inset-x-4 bottom-4 flex flex-wrap gap-2"
        >
          <span
            v-for="category in getCategorySummary(currentItem)"
            :key="category.label"
            class="rounded-full border px-2.5 py-1 text-[11px] font-medium backdrop-blur-sm"
            :style="{
              borderColor: category.color + '66',
              backgroundColor: category.color + '22',
              color: '#f8fafc',
            }"
          >
            {{ category.label }} × {{ category.count }}
          </span>
        </div>
      </div>
      <div
        v-else
        class="rounded-3xl border border-dashed border-white/10 bg-[#08101f]/80 py-24 text-center text-gray-500"
      >
        检测结果将在此处生成，当前未选中图片。
      </div>
    </div>

    <div class="overflow-x-auto py-2">
      <div class="flex gap-3 min-w-max">
        <button
          v-for="(item, index) in items"
          :key="item.id"
          @click="$emit('select', index)"
          type="button"
          class="relative min-w-[160px] rounded-3xl border p-2 text-left transition-all duration-300"
          :class="
            selectedIndex === index
              ? 'border-cyan-400 shadow-[0_0_30px_rgba(0,212,255,0.2)]'
              : 'border-white/10 hover:border-primary/50'
          "
        >
          <img
            :src="item.resultImage"
            alt="thumb"
            class="h-24 w-full rounded-3xl object-cover object-center"
          />
          <div class="mt-2 text-xs text-gray-300 font-medium">
            {{ item.fileName }}
          </div>
          <div
            class="mt-2 flex flex-wrap items-center gap-1.5 text-[11px] text-gray-500"
          >
            <span>{{ item.detections.length }} 缺陷</span>
            <span
              class="inline-block h-2 w-2 rounded-full"
              :class="getSeverityColor(item)"
            />
            <span
              v-if="item.detections.length"
              class="ml-1 flex flex-wrap gap-1"
            >
              <span
                v-for="category in getCategorySummary(item).slice(0, 2)"
                :key="category.label"
                class="rounded-full px-1.5 py-0.5"
                :style="{
                  backgroundColor: category.color + '22',
                  color: category.color,
                }"
              >
                {{ category.label }}
              </span>
            </span>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { DetectionItem } from "../data/detection.ts";
import ImageViewer from "./ImageViewer.vue";

const props = defineProps({
  items: { type: Array as () => DetectionItem[], default: () => [] },
  selectedIndex: { type: Number, default: 0 },
});

defineEmits<{
  (e: "select", index: number): void;
}>();

const currentItem = computed(() => props.items[props.selectedIndex] || null);

const getCategorySummary = (item: DetectionItem) => {
  const summary = new Map<
    string,
    { label: string; count: number; color: string }
  >();

  item.detections.forEach((box) => {
    const existing = summary.get(box.label);
    if (existing) {
      existing.count += 1;
      return;
    }

    summary.set(box.label, {
      label: box.label,
      count: 1,
      color: box.color,
    });
  });

  return Array.from(summary.values());
};

const getSeverityColor = (item: DetectionItem) => {
  const high = item.detections.some((box) => box.severity === "high");
  if (high) return "bg-red-500";
  const medium = item.detections.some((box) => box.severity === "medium");
  return medium ? "bg-yellow-400" : "bg-green-400";
};
</script>
