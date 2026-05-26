<template>
  <DashboardLayout>
    <div class="space-y-6 pb-10">
      <section class="space-y-6">
        <div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
          <div>
            <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
              <span>工作台</span>
              <span class="text-gray-600">›</span>
              <span class="text-primary">智能检测</span>
            </div>
            <h1 class="text-3xl font-bold text-white">批量缺陷检测工作台</h1>
            <p class="mt-2 text-gray-400 max-w-2xl">
              支持批量上传钢材表面图片，实时模拟检测进度，智能预览缺陷框和分类统计，帮助生产线快速定位异常。
            </p>
          </div>

          <div class="grid grid-cols-3 gap-3 w-full xl:w-auto">
            <div class="glass-card p-4 rounded-3xl border border-primary/20">
              <div class="text-sm text-gray-400">已上传</div>
              <div class="text-2xl font-semibold text-white">{{ totalImages }}</div>
            </div>
            <div class="glass-card p-4 rounded-3xl border border-primary/20">
              <div class="text-sm text-gray-400">缺陷总数</div>
              <div class="text-2xl font-semibold text-white">{{ totalDefects }}</div>
            </div>
            <div class="glass-card p-4 rounded-3xl border border-primary/20">
              <div class="text-sm text-gray-400">平均置信度</div>
              <div class="text-2xl font-semibold text-white">{{ (averageConfidence * 100).toFixed(1) }}%</div>
            </div>
          </div>
        </div>

        <div class="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div class="space-y-6">
            <BatchUploadPanel
              :items="store.items"
              :selectedIndex="store.selectedIndex"
              :totalItems="totalImages"
              :maxFiles="store.maxFiles"
              :maxSizeMB="store.maxSizeMB"
              :errors="store.errors"
              @upload="handleUpload"
              @select="handleSelect"
              @delete="handleDelete"
              @clear="handleClear"
            />

            <UploadToolbar
              :totalItems="totalImages"
              :maxFiles="store.maxFiles"
              :progress="store.batchProgress"
              :isBusy="store.isDetecting"
              :isPaused="store.isPaused"
              :hasItems="hasItems"
              @start="handleBatchStart"
              @pause="handlePause"
              @deleteSelected="handleDeleteSelected"
              @export="handleExport"
            />

            <div class="glass-card p-6 rounded-3xl border border-primary/20">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h2 class="text-lg font-semibold text-white">当前选中</h2>
                  <p class="text-gray-400 text-sm">实时检测状态与时间线</p>
                </div>
                <span class="rounded-full bg-white/5 px-3 py-2 text-xs text-gray-300">
                  {{ currentStatus }}
                </span>
              </div>
              <div class="space-y-3">
                <div class="flex items-center justify-between text-sm text-gray-400">
                  <span>选中图片</span>
                  <span>{{ store.selectedItem?.fileName || '无' }}</span>
                </div>
                <div class="flex items-center justify-between text-sm text-gray-400">
                  <span>检测进度</span>
                  <span>{{ store.selectedItem?.progress ?? 0 }}%</span>
                </div>
                <div class="flex items-center justify-between text-sm text-gray-400">
                  <span>当前状态</span>
                  <span class="capitalize">{{ store.selectedItem?.status || '待上传' }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-6">
            <DetectionStats
              :totalImages="totalImages"
              :totalDefects="totalDefects"
              :averageConfidence="averageConfidence"
              :completedCount="completedCount"
              :categorySummary="store.categorySummary"
            />

            <ImageGallery
              :items="store.items"
              :selectedIndex="store.selectedIndex"
              @select="handleSelect"
            />

            <DetectionGallery
              :items="store.items"
              :selectedIndex="store.selectedIndex"
              @select="handleSelect"
            />
          </div>
        </div>
      </section>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useBatchDetectionStore } from "../stores/batchDetection";
import DashboardLayout from "../layouts/DashboardLayout.vue";
import BatchUploadPanel from "../components/BatchUploadPanel.vue";
import UploadToolbar from "../components/UploadToolbar.vue";
import ImageGallery from "../components/ImageGallery.vue";
import DetectionGallery from "../components/DetectionGallery.vue";
import DetectionStats from "../components/DetectionStats.vue";

const store = useBatchDetectionStore();

const totalImages = computed(() => store.selectedCount);
const totalDefects = computed(() => store.totalDefects);
const averageConfidence = computed(() => store.averageConfidence);
const completedCount = computed(() => store.items.filter((item) => item.status === "completed").length);
const hasItems = computed(() => store.items.length > 0);
const currentStatus = computed(() => {
  if (store.isPaused) return "已暂停";
  if (store.isDetecting) return "检测中";
  if (store.items.length) return "就绪";
  return "等待上传";
});

const handleUpload = (files: FileList | File[]) => {
  store.addFiles(files);
};

const handleSelect = (index: number) => {
  store.selectIndex(index);
};

const handleDelete = (id: string) => {
  store.removeItem(id);
};

const handleClear = () => {
  store.clearAll();
};

const handleBatchStart = () => {
  store.detectAll();
};

const handlePause = () => {
  store.pauseDetection();
};

const handleExport = () => {
  store.exportResults();
};

const handleDeleteSelected = () => {
  if (store.selectedItem) {
    store.removeItem(store.selectedItem.id);
  }
};
</script>
