<template>
  <div class="glass-card p-6 space-y-5">
    <div class="flex items-center justify-between gap-4">
      <div>
        <h3 class="text-lg font-semibold text-white">批量上传</h3>
        <p class="text-gray-400 text-sm">拖拽或点击上传多张钢材表面图片。</p>
      </div>
      <div class="text-right text-sm text-gray-400">
        <div>最大 {{ maxFiles }} 张</div>
        <div>单张 ≤ {{ maxSizeMB }}MB</div>
      </div>
    </div>

    <div
      class="rounded-3xl border border-primary/20 bg-[#091323]/80 p-6 text-center transition-all duration-300 hover:border-primary/50 hover:bg-primary/10"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      :class="{ 'border-cyan-400/40 bg-cyan-500/10': dragging }"
    >
      <div
        class="mx-auto mb-4 inline-flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary"
      >
        <svg
          class="w-8 h-8"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
          />
        </svg>
      </div>
      <div class="text-white font-semibold text-lg">拖拽图片到此处</div>
      <div class="text-gray-400 text-sm mt-2">或</div>
      <button
        @click="triggerFileInput"
        class="mt-4 px-5 py-3 rounded-2xl bg-gradient-to-r from-primary to-cyan-400 text-sm font-medium text-white hover:shadow-lg hover:shadow-primary/30 transition-all"
      >
        选择文件上传
      </button>
      <input
        ref="fileInput"
        type="file"
        accept="image/jpeg,image/png,image/jpg"
        multiple
        class="hidden"
        @change="handleSelect"
      />
    </div>

    <div class="space-y-3">
      <div class="flex items-center justify-between text-sm text-gray-400">
        <span>已上传图片</span>
        <span>{{ totalItems }} / {{ maxFiles }}</span>
      </div>
      <div class="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-4">
        <button
          v-for="(item, index) in items"
          :key="item.id"
          @click="$emit('select', index)"
          type="button"
          class="group relative overflow-hidden rounded-3xl border p-1 transition-all duration-300"
          :class="
            selectedIndex === index
              ? 'border-cyan-400 shadow-[0_0_20px_rgba(0,212,255,0.25)]'
              : 'border-white/10 hover:border-primary/50'
          "
        >
          <img
            :src="item.originalImage"
            alt="thumb"
            class="h-28 w-full rounded-3xl object-cover object-center transition-transform duration-300 group-hover:scale-105"
          />
          <span
            class="absolute left-2 top-2 rounded-full bg-black/60 px-2 py-1 text-[11px] text-white"
            >{{ item.status }}</span
          >
          <button
            type="button"
            @click.stop="$emit('delete', item.id)"
            class="absolute right-2 bottom-2 inline-flex h-7 w-7 items-center justify-center rounded-full bg-black/70 text-white text-xs hover:bg-red-500"
          >
            ×
          </button>
        </button>
      </div>
      <div class="flex items-center justify-between gap-3">
        <button
          @click="$emit('clear')"
          :disabled="!items.length"
          class="flex-1 rounded-2xl border border-red-500/20 px-4 py-3 text-sm text-red-300 hover:bg-red-500/10 disabled:opacity-40 transition-all"
        >
          清空全部
        </button>
        <div class="text-xs text-gray-400">
          <p>
            当前选中：{{
              selectedIndex >= 0 && items[selectedIndex]
                ? items[selectedIndex].fileName
                : "无"
            }}
          </p>
        </div>
      </div>
    </div>

    <div
      v-if="errors.length"
      class="rounded-3xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-200"
    >
      <div class="font-semibold mb-2">警告</div>
      <ul class="space-y-1 list-disc list-inside">
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { DetectionItem } from "../mock/detection";

defineProps({
  items: { type: Array as () => DetectionItem[], default: () => [] },
  selectedIndex: { type: Number, default: 0 },
  totalItems: { type: Number, default: 0 },
  maxFiles: { type: Number, default: 10 },
  maxSizeMB: { type: Number, default: 6 },
  errors: { type: Array as () => string[], default: () => [] },
});

const emit = defineEmits<{
  (e: "upload", files: FileList): void;
  (e: "select", index: number): void;
  (e: "delete", id: string): void;
  (e: "clear"): void;
}>();

const fileInput = ref<HTMLInputElement | null>(null);
const dragging = ref(false);

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    emit("upload", target.files);
    target.value = "";
  }
};

const onDragOver = () => {
  dragging.value = true;
};

const onDragLeave = () => {
  dragging.value = false;
};

const onDrop = (event: DragEvent) => {
  dragging.value = false;
  if (!event.dataTransfer) return;
  emit("upload", event.dataTransfer.files);
};
</script>
