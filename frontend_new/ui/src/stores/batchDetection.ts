import { defineStore } from "pinia";
import { ref, computed } from "vue";
import {
  buildMockDetectionResult,
  createDetectionItem,
  DetectionItem,
} from "../mock/detection";

export const useBatchDetectionStore = defineStore("batchDetection", () => {
  const items = ref<DetectionItem[]>([]);
  const selectedIndex = ref(0);
  const isDetecting = ref(false);
  const isPaused = ref(false);
  const errors = ref<string[]>([]);
  const maxFiles = 10;
  const maxSizeMB = 6;

  const selectedItem = computed(() => items.value[selectedIndex.value] || null);

  const batchProgress = computed(() => {
    if (!items.value.length) return 0;
    const total = items.value.reduce((sum, item) => sum + item.progress, 0);
    return Math.round(total / items.value.length);
  });

  const totalDefects = computed(() => {
    return items.value.reduce((sum, item) => sum + item.detections.length, 0);
  });

  const averageConfidence = computed(() => {
    const all = items.value.flatMap((item) => item.detections);
    if (!all.length) return 0;
    return Number(
      (all.reduce((sum, box) => sum + box.confidence, 0) / all.length).toFixed(
        2,
      ),
    );
  });

  const categorySummary = computed(() => {
    const stats = new Map<string, number>();
    items.value.forEach((item) => {
      item.detections.forEach((box) => {
        stats.set(box.label, (stats.get(box.label) || 0) + 1);
      });
    });
    return Array.from(stats.entries()).map(([label, count]) => ({
      label,
      count,
    }));
  });

  const selectedCount = computed(() => items.value.length);

  const isIdle = computed(
    () =>
      !items.value.length ||
      items.value.every((item) => item.status === "completed"),
  );

  const addFiles = async (fileList: FileList | File[]) => {
    const files = Array.from(fileList);
    const availableSlots = maxFiles - items.value.length;
    const accepted = files.slice(0, availableSlots);

    if (files.length > availableSlots) {
      errors.value.push(`最多只能上传 ${maxFiles} 张图片，已跳过多余文件。`);
    }

    const createdItems = await Promise.all(
      accepted.map(async (file) => {
        if (!file.type.startsWith("image/")) {
          errors.value.push(`${file.name} 不是有效图片格式。`);
          return null;
        }
        if (file.size > maxSizeMB * 1024 * 1024) {
          errors.value.push(`${file.name} 超过 ${maxSizeMB}MB 限制。`);
          return null;
        }
        try {
          return await createDetectionItem(file);
        } catch {
          errors.value.push(`${file.name} 读取失败。`);
          return null;
        }
      }),
    );

    items.value.push(...(createdItems.filter(Boolean) as DetectionItem[]));
    if (selectedIndex.value >= items.value.length) {
      selectedIndex.value = Math.max(0, items.value.length - 1);
    }
  };

  const removeItem = (id: string) => {
    const index = items.value.findIndex((item) => item.id === id);
    if (index < 0) return;
    items.value.splice(index, 1);
    if (selectedIndex.value >= items.value.length) {
      selectedIndex.value = Math.max(0, items.value.length - 1);
    }
  };

  const clearAll = () => {
    items.value = [];
    selectedIndex.value = 0;
    isDetecting.value = false;
    isPaused.value = false;
    errors.value = [];
  };

  const selectIndex = (index: number) => {
    if (index < 0 || index >= items.value.length) return;
    selectedIndex.value = index;
  };

  const pauseDetection = () => {
    isPaused.value = !isPaused.value;
    if (isPaused.value) {
      isDetecting.value = false;
    }
  };

  const simulateDetection = (item: DetectionItem) => {
    return new Promise<void>((resolve) => {
      const steps = 14;
      let current = 0;
      const interval = window.setInterval(() => {
        if (isPaused.value) {
          window.clearInterval(interval);
          item.status = "paused";
          isDetecting.value = false;
          resolve();
          return;
        }

        current += 1;
        item.progress = Math.min(100, Math.round((current / steps) * 100));
        item.status = "running";
        item.updatedAt = Date.now();

        if (current >= steps) {
          window.clearInterval(interval);
          const completed = buildMockDetectionResult(item);
          item.detections = completed.detections;
          item.status = "completed";
          item.progress = 100;
          item.updatedAt = Date.now();
          resolve();
        }
      }, 140);
    });
  };

  const detectAll = async () => {
    if (!items.value.length) return;
    if (isDetecting.value) return;
    isDetecting.value = true;
    isPaused.value = false;

    for (let index = 0; index < items.value.length; index += 1) {
      const item = items.value[index];
      if (item.status === "completed") continue;
      if (isPaused.value) break;
      selectedIndex.value = index;
      await simulateDetection(item);
    }

    isDetecting.value = false;
  };

  const exportResults = () => {
    const payload = items.value.map((item) => ({
      id: item.id,
      fileName: item.fileName,
      fileSize: item.fileSize,
      status: item.status,
      progress: item.progress,
      detections: item.detections,
    }));
    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: "application/json",
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `batch-detection-${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return {
    items,
    selectedIndex,
    selectedItem,
    isDetecting,
    isPaused,
    errors,
    maxFiles,
    maxSizeMB,
    batchProgress,
    totalDefects,
    averageConfidence,
    categorySummary,
    selectedCount,
    isIdle,
    addFiles,
    removeItem,
    clearAll,
    selectIndex,
    pauseDetection,
    detectAll,
    exportResults,
  };
});
