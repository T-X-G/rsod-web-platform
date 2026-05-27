<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
    @click.self="closeDialog"
  >
    <div
      class="relative max-w-6xl w-full max-h-[90vh] rounded-3xl border border-primary/20 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 shadow-2xl overflow-hidden"
    >
      <!-- Header -->
      <div
        class="flex items-center justify-between p-6 border-b border-primary/10"
      >
        <div>
          <h2 class="text-2xl font-bold text-white">{{ task.task_name }}</h2>
          <p class="text-sm text-gray-400 mt-1">
            {{ formatTime(task.created_at) }} · {{ task.total_images }} 张图片 ·
            {{ task.total_defects }} 个缺陷
          </p>
        </div>
        <button
          @click="closeDialog"
          class="text-gray-400 hover:text-white transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="flex h-[calc(90vh-120px)] overflow-hidden">
        <!-- Main Image Area -->
        <div class="flex-1 flex flex-col border-r border-primary/10">
          <!-- Mode Tabs -->
          <div class="flex gap-4 p-4 border-b border-primary/10 bg-black/20">
            <button
              v-for="mode in ['original', 'result']"
              :key="mode"
              @click="viewMode = (mode as 'original' | 'result')"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                viewMode === mode
                  ? 'bg-primary/30 text-primary border border-primary/50'
                  : 'text-gray-400 hover:text-gray-300',
              ]"
            >
              {{ mode === "original" ? "原始图" : "检测结果图" }}
            </button>
          </div>

          <!-- Image Viewer -->
          <div
            class="flex-1 flex items-center justify-center bg-black/40 p-4 overflow-auto"
          >
            <div
              v-if="currentImage"
              class="w-full h-full flex items-center justify-center"
            >
              <img
                :src="currentImage.result_image_url"
                :alt="currentImage.filename"
                class="max-w-full max-h-full object-contain rounded-2xl shadow-lg"
              />
            </div>
            <div v-else class="text-gray-500">暂无图片</div>
          </div>

          <!-- Thumbnail Navigation -->
          <div
            class="border-t border-primary/10 bg-black/40 p-4 overflow-x-auto"
          >
            <div class="flex gap-3 min-w-max">
              <button
                v-for="(img, idx) in task.images"
                :key="img.record_id"
                @click="selectedImageIndex = idx"
                :class="[
                  'relative min-w-[100px] rounded-2xl border p-2 transition-all',
                  selectedImageIndex === idx
                    ? 'border-cyan-400 shadow-[0_0_20px_rgba(0,212,255,0.2)]'
                    : 'border-white/10 hover:border-primary/50',
                ]"
              >
                <img
                  :src="img.result_image_url"
                  alt="thumb"
                  class="w-full h-20 rounded-lg object-cover"
                />
                <div class="mt-1 text-[10px] text-gray-400 truncate">
                  {{ img.filename }}
                </div>
                <div class="text-[9px] text-gray-500">
                  {{ img.boxes.length }} 缺陷
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Right Sidebar: Stats & Details -->
        <div
          class="w-80 border-l border-primary/10 bg-black/30 overflow-y-auto"
        >
          <!-- Task Stats -->
          <div class="p-6 border-b border-primary/10 space-y-4">
            <div>
              <div class="text-xs uppercase tracking-wider text-gray-500 mb-3">
                任务统计
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div class="p-3 bg-white/5 rounded-xl border border-primary/10">
                  <div class="text-gray-400 text-xs mb-1">总缺陷数</div>
                  <div class="text-2xl font-bold text-white">
                    {{ task.total_defects }}
                  </div>
                </div>
                <div class="p-3 bg-white/5 rounded-xl border border-primary/10">
                  <div class="text-gray-400 text-xs mb-1">平均置信度</div>
                  <div class="text-2xl font-bold text-primary">
                    {{ (task.average_confidence * 100).toFixed(1) }}%
                  </div>
                </div>
              </div>
            </div>

            <div>
              <div class="text-xs uppercase tracking-wider text-gray-500 mb-3">
                任务状态
              </div>
              <div class="flex items-center gap-2">
                <div
                  :class="[
                    'w-3 h-3 rounded-full',
                    task.status === 'completed'
                      ? 'bg-green-500'
                      : task.status === 'processing'
                        ? 'bg-yellow-500 animate-pulse'
                        : 'bg-red-500',
                  ]"
                />
                <span class="text-gray-300 text-sm">
                  {{
                    task.status === "completed"
                      ? "已完成"
                      : task.status === "processing"
                        ? "进行中"
                        : "失败"
                  }}
                </span>
              </div>
            </div>
          </div>

          <!-- Current Image Details -->
          <div
            class="p-6 border-b border-primary/10 space-y-4"
            v-if="currentImage"
          >
            <div>
              <div class="text-xs uppercase tracking-wider text-gray-500 mb-3">
                当前图片
              </div>
              <div class="text-sm text-white font-medium truncate">
                {{ currentImage.filename }}
              </div>
              <div class="text-xs text-gray-400 mt-1">
                {{ currentImage.boxes.length }} 个缺陷
              </div>
            </div>

            <!-- Defect Categories -->
            <div v-if="currentImage.boxes.length > 0">
              <div class="text-xs uppercase tracking-wider text-gray-500 mb-3">
                缺陷类别
              </div>
              <div class="space-y-2">
                <div
                  v-for="category in getImageCategories(currentImage)"
                  :key="category.label"
                  class="p-3 rounded-lg border"
                  :style="{
                    borderColor: category.color + '66',
                    backgroundColor: category.color + '11',
                  }"
                >
                  <div class="flex items-center justify-between">
                    <span class="text-sm text-gray-300">{{
                      category.label
                    }}</span>
                    <span
                      class="text-xs font-medium px-2 py-1 rounded-full"
                      :style="{
                        backgroundColor: category.color + '33',
                        color: category.color,
                      }"
                    >
                      × {{ category.count }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Confidence Details -->
            <div v-if="currentImage.boxes.length > 0">
              <div class="text-xs uppercase tracking-wider text-gray-500 mb-3">
                置信度
              </div>
              <div class="space-y-2">
                <div
                  v-for="(box, idx) in currentImage.boxes"
                  :key="idx"
                  class="flex items-center justify-between text-xs"
                >
                  <span class="text-gray-400">{{ box.chinese_name || box.class_name }}</span>
                  <div class="flex items-center gap-2">
                    <div
                      class="w-20 h-2 rounded-full bg-white/10 overflow-hidden"
                    >
                      <div
                        class="h-full rounded-full bg-cyan-400 transition-all"
                        :style="{
                          width: `${box.confidence * 100}%`,
                        }"
                      />
                    </div>
                    <span class="text-gray-500 w-12 text-right">
                      {{ (box.confidence * 100).toFixed(0) }}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Category Summary -->
          <div class="p-6 space-y-3">
            <div class="text-xs uppercase tracking-wider text-gray-500 mb-3">
              全部缺陷分布
            </div>
            <div
              v-for="category in getAllCategories()"
              :key="category.label"
              class="flex items-center justify-between text-xs"
            >
              <span class="text-gray-400">{{ category.label }}</span>
              <div class="flex items-center gap-2">
                <div
                  class="w-16 h-1.5 rounded-full bg-white/10 overflow-hidden"
                >
                  <div
                    class="h-full rounded-full"
                    :style="{
                      backgroundColor: category.color,
                      width: `${getCategoryRatio(category.count)}%`,
                    }"
                  />
                </div>
                <span class="text-gray-500 w-8 text-right">
                  {{ category.count }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { DetectionBox } from "../data/detection";

interface TaskImage {
  record_id: string; filename: string; total_objects: number;
  result_image_url: string; boxes: DetectionBox[]; status: string;
  created_at: string; detection_time?: number;
}
interface DetailTask {
  task_id: string; task_name: string; total_images: number; total_defects: number;
  average_confidence: number; status: string; created_at: string;
  images?: TaskImage[];
}

const props = defineProps<{
  isOpen: boolean;
  task: DetailTask;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const selectedImageIndex = ref(0);
const viewMode = ref<"original" | "result">("original");

const currentImage = computed(
  () => (props.task.images || [])[selectedImageIndex.value] || null,
);

const getImageCategories = (image: TaskImage) => {
  const summary = new Map<string, { label: string; count: number; color: string }>();
  image.boxes.forEach((box: DetectionBox) => {
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

const getAllCategories = () => {
  const summary = new Map<
    string,
    { label: string; count: number; color: string }
  >();
  props.task.images?.forEach((img) => {
    img.boxes.forEach((box) => {
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
  });
  return Array.from(summary.values());
};

const getCategoryRatio = (count: number) => {
  if (!props.task.total_defects) return 0;
  return Math.min(100, Math.round((count / props.task.total_defects) * 100));
};

const formatTime = (t: string | number) => {
  if (!t) return "";
  if (typeof t === "number") return new Date(t).toLocaleString("zh-CN");
  return new Date(t).toLocaleString("zh-CN");
};

const closeDialog = () => {
  emit("close");
};
</script>
