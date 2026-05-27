import { defineStore } from "pinia";
import { ref, computed } from "vue";
import {
  type DetectionBox,
  type DetectionItem,
  createDetectionItem,
} from "../data/detection";

// ============ Task Data Structures ============
export interface DetectionImage {
  id: string;
  fileName: string;
  originalImage: string;
  resultImage: string;
  detections: DetectionBox[];
  status: "pending" | "running" | "completed" | "paused" | "failed";
  progress: number;
  detectTime?: number;
}

export interface DetectionTask {
  id: string;
  taskName: string;
  createdAt: number;
  updatedAt: number;
  status: "processing" | "completed" | "failed";
  totalImages: number;
  totalDefects: number;
  averageConfidence: number;
  images: DetectionImage[];
}

const DEFECT_CONFIG: Record<
  string,
  { severity: DetectionBox["severity"]; color: string }
> = {
  crazing: { severity: "high", color: "#ef4444" },
  inclusion: { severity: "high", color: "#8b5cf6" },
  patches: { severity: "medium", color: "#f59e0b" },
  pitted_surface: { severity: "medium", color: "#3b82f6" },
  "rolled-in_scale": { severity: "medium", color: "#f97316" },
  scratches: { severity: "low", color: "#22c55e" },
};

function mapApiBox(box: {
  bbox: [number, number, number, number];
  confidence: number;
  class_name: string;
  chinese_name: string;
}): DetectionBox {
  const config =
    DEFECT_CONFIG[box.class_name] ??
    ({ severity: "medium", color: "#6b7280" } as any);
  return {
    label: box.chinese_name || box.class_name,
    confidence: Number(box.confidence.toFixed(2)),
    bbox: box.bbox,
    severity: config.severity,
    color: config.color,
  };
}

function makeProxyUrl(url: string): string {
  if (!url) return "";
  try {
    return new URL(url).pathname;
  } catch {
    return url;
  }
}

async function callDetectionApi(file: File): Promise<{
  boxes: DetectionBox[];
  resultImage: string;
  originalImage: string;
}> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("model_name", "steel-defect-yolo11n");

  const token = localStorage.getItem("token");
  const response = await fetch("/api/detection/single", {
    method: "POST",
    body: formData,
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  const json = await response.json();
  if (!json.success || !json.data) {
    throw new Error(json.message || "detection failed");
  }

  const data = json.data;
  return {
    boxes: (data.boxes || []).map(mapApiBox),
    resultImage: makeProxyUrl(data.result_image_url),
    originalImage: makeProxyUrl(data.image_url),
  };
}

export const useBatchDetectionStore = defineStore("batchDetection", () => {
  const items = ref<DetectionItem[]>([]);
  const fileMap = new Map<string, File>();
  const selectedIndex = ref(0);
  const isDetecting = ref(false);
  const isPaused = ref(false);
  const errors = ref<string[]>([]);
  const maxFiles = 10;
  const maxSizeMB = 6;

  // ============ Task Management ============
  const detectionTasks = ref<DetectionTask[]>([]);
  const currentTask = ref<DetectionTask | null>(null);

  // Load tasks from localStorage on store creation
  const loadTasksFromStorage = () => {
    try {
      const stored = localStorage.getItem("detectionTasks");
      if (stored) {
        detectionTasks.value = JSON.parse(stored);
      }
    } catch (e) {
      console.error("Failed to load tasks from localStorage:", e);
    }
  };

  const saveTasksToStorage = () => {
    try {
      localStorage.setItem(
        "detectionTasks",
        JSON.stringify(detectionTasks.value),
      );
    } catch (e) {
      console.error("Failed to save tasks to localStorage:", e);
    }
  };

  const createDetectionTask = (): DetectionTask => {
    const now = Date.now();
    const taskId = `task-${now}-${Math.random().toString(36).slice(2, 10)}`;
    const task: DetectionTask = {
      id: taskId,
      taskName: `批量检测 ${new Date(now).toLocaleString("zh-CN")}`,
      createdAt: now,
      updatedAt: now,
      status: "processing",
      totalImages: items.value.length,
      totalDefects: 0,
      averageConfidence: 0,
      images: items.value.map((item) => ({
        id: item.id,
        fileName: item.fileName,
        originalImage: item.originalImage,
        resultImage: item.resultImage,
        detections: [...item.detections],
        status: item.status,
        progress: item.progress,
        detectTime: undefined,
      })),
    };
    return task;
  };

  const updateTaskStats = (task: DetectionTask) => {
    const allDetections = task.images.flatMap((img) => img.detections);
    task.totalDefects = allDetections.length;
    task.totalImages = task.images.length;
    task.averageConfidence =
      allDetections.length > 0
        ? Number(
            (
              allDetections.reduce((sum, box) => sum + box.confidence, 0) /
              allDetections.length
            ).toFixed(2),
          )
        : 0;
    task.updatedAt = Date.now();

    // Update task status based on images
    const allCompleted = task.images.every((img) => img.status === "completed");
    const anyFailed = task.images.some((img) => img.status === "failed");
    if (anyFailed && allCompleted) {
      task.status = "failed";
    } else if (allCompleted) {
      task.status = "completed";
    }
  };

  const appendTaskResult = (taskId: string, imageId: string) => {
    const task = detectionTasks.value.find((t) => t.id === taskId);
    if (!task) return;

    const item = items.value.find((i) => i.id === imageId);
    if (!item) return;

    // Update the image in task
    const taskImage = task.images.find((img) => img.id === imageId);
    if (taskImage) {
      taskImage.resultImage = item.resultImage;
      taskImage.detections = [...item.detections];
      taskImage.status = item.status;
      taskImage.progress = item.progress;
      taskImage.detectTime = item.updatedAt;
    }

    // Recalculate task stats
    updateTaskStats(task);
    saveTasksToStorage();
  };

  // Initialize on first access
  loadTasksFromStorage();

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
          const item = await createDetectionItem(file);
          fileMap.set(item.id, file);
          return item;
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
    fileMap.delete(id);
    if (selectedIndex.value >= items.value.length) {
      selectedIndex.value = Math.max(0, items.value.length - 1);
    }
  };

  const clearAll = () => {
    items.value = [];
    fileMap.clear();
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

  const runDetection = async (item: DetectionItem) => {
    try {
      item.status = "running";
      item.progress = 30;

      const file = fileMap.get(item.id);
      if (!file) throw new Error("no file reference");

      const result = await callDetectionApi(file);

      item.detections = result.boxes;
      item.resultImage = result.resultImage;
      item.status = "completed";
      item.progress = 100;
      item.updatedAt = Date.now();

      // Update current task if exists
      if (currentTask.value) {
        appendTaskResult(currentTask.value.id, item.id);
      }
    } catch (e: unknown) {
      item.status = "failed";
      item.progress = 0;
      errors.value.push(
        `${item.fileName}: ${(e as Error).message || "detection failed"}`,
      );

      // Update current task status on error
      if (currentTask.value) {
        appendTaskResult(currentTask.value.id, item.id);
      }
    }
  };

  const detectAll = async () => {
    if (!items.value.length) return;
    if (isDetecting.value) return;
    isDetecting.value = true;
    isPaused.value = false;

    // Create a new detection task
    const task = createDetectionTask();
    currentTask.value = task;
    detectionTasks.value.push(task);
    saveTasksToStorage();

    for (let index = 0; index < items.value.length; index += 1) {
      const item = items.value[index];
      if (item.status === "completed") continue;
      if (isPaused.value) break;
      selectedIndex.value = index;
      await runDetection(item);
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
    // Current batch
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

    // Tasks management
    detectionTasks,
    currentTask,
    createDetectionTask,
    updateTaskStats,
    appendTaskResult,
    saveTasksToStorage,
    loadTasksFromStorage,
  };
});
