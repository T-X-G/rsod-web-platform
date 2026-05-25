<template>
  <div class="glass-card p-6 space-y-4">
    <div class="flex items-center justify-between gap-4 mb-4">
      <div>
        <h3 class="text-lg font-semibold text-white">原始图片预览</h3>
        <p class="text-gray-400 text-sm">点击缩略图切换当前检视原图。</p>
      </div>
      <div class="text-xs text-gray-400">可滚轮缩放 / 双击重置</div>
    </div>

    <div class="space-y-4">
      <ImageViewer
        v-if="currentItem"
        :src="currentItem.originalImage"
        :alt="currentItem.fileName"
      />
      <div
        v-else
        class="rounded-3xl border border-dashed border-white/10 bg-[#08101f]/80 py-24 text-center text-gray-500"
      >
        暂无原图，请上传图片后开始批量检测。
      </div>
    </div>

    <div class="overflow-x-auto py-2">
      <div class="flex gap-3 min-w-max">
        <button
          v-for="(item, index) in items"
          :key="item.id"
          @click="$emit('select', index)"
          type="button"
          class="relative min-w-[120px] rounded-3xl border p-2 text-left transition-all duration-300"
          :class="
            selectedIndex === index
              ? 'border-cyan-400 shadow-[0_0_30px_rgba(0,212,255,0.2)]'
              : 'border-white/10 hover:border-primary/50'
          "
        >
          <img
            :src="item.originalImage"
            alt="thumb"
            class="h-24 w-full rounded-3xl object-cover object-center"
          />
          <div class="mt-2 text-xs text-gray-300 font-medium">
            {{ item.fileName }}
          </div>
          <div class="mt-1 text-[11px] text-gray-500">
            {{ (item.fileSize / 1024 / 1024).toFixed(2) }} MB
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { DetectionItem } from "../mock/detection";
import ImageViewer from "./ImageViewer.vue";

const props = defineProps({
  items: { type: Array as () => DetectionItem[], default: () => [] },
  selectedIndex: { type: Number, default: 0 },
});

defineEmits<{
  (e: "select", index: number): void;
}>();

const currentItem = computed(() => props.items[props.selectedIndex] || null);
</script>
