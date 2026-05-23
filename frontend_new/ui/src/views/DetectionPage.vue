<template>
  <DashboardLayout>
    <div class="space-y-6">
      <!-- Part 1: Header & Detection Area -->
      <section class="space-y-6">
        <!-- Page Header -->
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
              <span>工作台</span>
              <span class="text-gray-600">›</span>
              <span class="text-primary">智能检测</span>
            </div>
            <h1 class="text-2xl font-bold text-white mb-2">
              上传钢材表面图片，立即识别缺陷
            </h1>
            <p class="text-gray-400">
              支持裂纹 / 夹杂物 / 斑点 / 麻面 / 轧入氧化皮 / 划痕等缺陷检测
            </p>
          </div>

          <!-- Model Selector -->
          <div class="glass-card px-4 py-2 flex items-center gap-3">
            <span class="text-gray-400 text-sm">检测模型</span>
            <select
              class="bg-transparent text-primary border-none focus:outline-none text-sm font-medium cursor-pointer"
            >
              <option value="rsod-yolo11n">rsod-yolo11n</option>
              <option value="yolo11s">yolo11s</option>
              <option value="yolo11m">yolo11m</option>
            </select>
          </div>
        </div>

        <!-- Detection Mode Toggle -->
        <div class="glass-card p-1 inline-flex">
          <button
            v-for="mode in detectionModes"
            :key="mode.id"
            @click="activeMode = mode.id"
            :class="[
              'flex items-center gap-3 px-6 py-4 rounded-xl transition-all duration-300',
              activeMode === mode.id
                ? 'bg-primary/20 text-primary border border-primary/30'
                : 'text-gray-400 hover:text-white hover:bg-white/5',
            ]"
          >
            <component :is="mode.icon" class="w-6 h-6" />
            <div class="text-left">
              <div class="font-medium">{{ mode.name }}</div>
              <div class="text-xs opacity-70">{{ mode.desc }}</div>
            </div>
          </button>
        </div>

        <!-- Detection Preview Section -->
        <div class="glass-card p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-white">检测预览</h2>
            <div class="flex items-center gap-2">
              <button
                v-for="view in viewModes"
                :key="view.id"
                @click="viewMode = view.id"
                :class="[
                  'px-4 py-2 rounded-lg text-sm transition-all duration-300',
                  viewMode === view.id
                    ? 'bg-primary/20 text-primary border border-primary/30'
                    : 'text-gray-400 hover:text-white border border-transparent',
                ]"
              >
                {{ view.name }}
              </button>
              <button
                class="flex items-center gap-2 px-4 py-2 text-gray-400 hover:text-primary transition-colors text-sm ml-4"
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
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                  />
                </svg>
                等待上传
              </button>
            </div>
          </div>

          <!-- Preview Grid -->
          <div
            :class="
              viewMode === 'side'
                ? 'grid grid-cols-2 gap-6'
                : 'grid grid-cols-1 gap-6'
            "
          >
            <!-- Original Image Area -->
            <div class="relative">
              <div
                class="aspect-[4/3] rounded-xl border-2 border-dashed border-primary/30 bg-[#0d1221]/50 flex flex-col items-center justify-center cursor-pointer hover:border-primary/50 hover:bg-primary/5 transition-all duration-300 group"
                @click="triggerUpload"
                @dragover.prevent="dragOver = true"
                @dragleave="dragOver = false"
                @drop.prevent="handleDrop"
                :class="{ 'border-primary bg-primary/10': dragOver }"
              >
                <div v-if="!uploadedImage" class="text-center">
                  <div
                    class="w-16 h-16 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform"
                  >
                    <svg
                      class="w-8 h-8 text-primary"
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
                  <p class="text-white font-medium mb-1">请上传图片</p>
                  <p class="text-gray-500 text-sm">支持 jpg、png 格式</p>
                </div>
                <img
                  v-else
                  :src="uploadedImage"
                  alt="Uploaded"
                  class="w-full h-full object-contain rounded-lg"
                />
              </div>
              <div
                class="absolute bottom-0 left-0 right-0 bg-gradient-to-r from-primary to-cyan-500 text-white text-center py-2 rounded-b-xl font-medium"
              >
                原始图片
              </div>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleFileSelect"
              />
            </div>

            <!-- Detection Result Area -->
            <div class="relative">
              <div
                class="aspect-[4/3] rounded-xl border border-primary/20 bg-[#0d1221]/50 flex flex-col items-center justify-center overflow-hidden"
              >
                <div v-if="!detectionResult" class="text-center">
                  <div
                    class="w-16 h-16 mx-auto mb-4 rounded-full bg-white/5 flex items-center justify-center"
                  >
                    <svg
                      class="w-8 h-8 text-gray-500"
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
                  </div>
                  <p class="text-gray-400 font-medium mb-1">
                    检测结果将在此展示
                  </p>
                  <p class="text-gray-600 text-sm">上传图片后开始检测</p>
                </div>
                <div v-else class="w-full h-full relative">
                  <img
                    :src="uploadedImage"
                    alt="Result"
                    class="w-full h-full object-contain"
                  />
                  <!-- Detection Boxes -->
                  <div
                    v-for="(box, idx) in detectionResult.boxes"
                    :key="idx"
                    class="absolute border-2 rounded"
                    :class="
                      box.severity === 'high'
                        ? 'border-red-500 bg-red-500/20'
                        : box.severity === 'medium'
                          ? 'border-yellow-500 bg-yellow-500/20'
                          : 'border-green-500 bg-green-500/20'
                    "
                    :style="{
                      left: box.x + '%',
                      top: box.y + '%',
                      width: box.w + '%',
                      height: box.h + '%',
                    }"
                  >
                    <span
                      class="absolute -top-6 left-0 text-white text-xs px-2 py-0.5 rounded whitespace-nowrap"
                      :class="
                        box.severity === 'high'
                          ? 'bg-red-500'
                          : box.severity === 'medium'
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                      "
                    >
                      {{ box.label }} {{ (box.confidence * 100).toFixed(1) }}%
                    </span>
                  </div>
                </div>
              </div>
              <div
                class="absolute bottom-0 left-0 right-0 bg-gradient-to-r from-primary to-cyan-500 text-white text-center py-2 rounded-b-xl font-medium"
              >
                检测结果
              </div>
            </div>
          </div>

          <!-- Start Detection Button -->
          <div
            v-if="uploadedImage && !detectionResult"
            class="mt-6 flex justify-center"
          >
            <button
              @click="startDetection"
              :disabled="isDetecting"
              class="px-8 py-3 bg-gradient-to-r from-primary to-cyan-400 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-primary/30 transition-all disabled:opacity-50 flex items-center gap-2"
            >
              <svg
                v-if="isDetecting"
                class="w-5 h-5 animate-spin"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              {{ isDetecting ? "检测中..." : "开始检测" }}
            </button>
          </div>
        </div>
      </section>

      <!-- Part 2: Model Info & Results -->
      <section class="space-y-6">
        <!-- Model Info Card -->
        <div class="glass-card p-6">
          <div class="flex items-center gap-3 mb-4">
            <div
              class="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-primary"
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
            </div>
            <h3 class="text-lg font-semibold text-white">检测模型信息</h3>
          </div>
          <div class="grid grid-cols-2 gap-8">
            <div
              class="flex justify-between items-center py-3 border-b border-primary/10"
            >
              <span class="text-gray-400">检测模型</span>
              <span class="text-primary font-medium">rsod-yolo11n</span>
            </div>
            <div
              class="flex justify-between items-center py-3 border-b border-primary/10"
            >
              <span class="text-gray-400">模型版本</span>
              <span class="text-white font-medium">v1.0.0</span>
            </div>
          </div>
        </div>

        <!-- Recognition List -->
        <div class="glass-card p-6">
          <div class="flex items-center gap-3 mb-4">
            <div
              class="w-10 h-10 rounded-xl bg-green-500/20 flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-green-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white">识别清单</h3>
          </div>

          <div v-if="!detectionResult" class="py-16 text-center">
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
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                />
              </svg>
            </div>
            <p class="text-white font-medium mb-1">请上传图片开始检测</p>
            <p class="text-gray-500 text-sm">上传钢材表面图片以识别缺陷</p>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="(box, idx) in detectionResult.boxes"
              :key="idx"
              class="flex items-center justify-between p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors border border-transparent hover:border-primary/20"
            >
              <div class="flex items-center gap-4">
                <div
                  :class="[
                    'w-3 h-3 rounded-full',
                    box.severity === 'high'
                      ? 'bg-red-500 shadow-lg shadow-red-500/50'
                      : box.severity === 'medium'
                        ? 'bg-yellow-500 shadow-lg shadow-yellow-500/50'
                        : 'bg-green-500 shadow-lg shadow-green-500/50',
                  ]"
                ></div>
                <span class="text-white font-medium">{{ box.label }}</span>
                <span
                  class="px-2 py-0.5 bg-primary/20 text-primary text-xs rounded-full"
                  >{{ box.type }}</span
                >
              </div>
              <div class="flex items-center gap-6">
                <span class="text-gray-400 text-sm"
                  >置信度:
                  <span class="text-white"
                    >{{ (box.confidence * 100).toFixed(1) }}%</span
                  ></span
                >
                <span class="text-gray-500 text-sm"
                  >位置: ({{ box.x }}, {{ box.y }})</span
                >
              </div>
            </div>
          </div>
        </div>

        <!-- AI Diagnosis -->
        <div class="glass-card p-6">
          <div class="flex items-center gap-3 mb-4">
            <div
              class="w-10 h-10 rounded-xl bg-purple-500/20 flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-purple-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white">AI 诊断建议</h3>
          </div>

          <div v-if="!detectionResult" class="py-8 text-center text-gray-500">
            上传图片后将自动生成诊断建议
          </div>

          <div v-else class="space-y-4">
            <div
              class="p-4 bg-gradient-to-r from-primary/10 to-purple-500/10 border border-primary/20 rounded-xl"
            >
              <p class="text-gray-300 leading-relaxed">
                检测到
                <span class="text-primary font-medium"
                  >{{ detectionResult.boxes.length }} 处</span
                >
                表面缺陷，其中包含
                <span class="text-red-400"
                  >{{
                    detectionResult.boxes.filter(
                      (b: any) => b.severity === "high",
                    ).length
                  }}
                  处高风险缺陷</span
                >，建议立即进行人工复检。 该批次钢材表面质量评级为
                <span class="text-yellow-400 font-medium">B级</span>，
                需要在后续工序中加强监控。检测耗时
                <span class="text-primary">{{ detectionResult.time }}ms</span>。
              </p>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="glass-card p-4">
          <div class="flex gap-4">
            <button
              @click="resetDetection"
              class="flex-1 flex items-center justify-center gap-2 py-4 rounded-xl border border-primary/30 text-primary hover:bg-primary/10 transition-all duration-300"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              重新检测
            </button>
            <button
              class="flex-1 flex items-center justify-center gap-2 py-4 rounded-xl bg-gradient-to-r from-primary to-cyan-400 text-white font-medium hover:shadow-lg hover:shadow-primary/30 transition-all duration-300"
            >
              查看完整报告
            </button>
          </div>
        </div>
      </section>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, h } from "vue";
import DashboardLayout from "../layouts/DashboardLayout.vue";

const activeMode = ref("single");
const viewMode = ref("side");
const uploadedImage = ref<string | undefined>(undefined);
const detectionResult = ref<any>(null);
const isDetecting = ref(false);
const dragOver = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

const detectionModes = [
  {
    id: "single",
    name: "单图检测",
    desc: "快速识别一张图片",
    icon: {
      render() {
        return h(
          "svg",
          { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
          [
            h("path", {
              "stroke-linecap": "round",
              "stroke-linejoin": "round",
              "stroke-width": "2",
              d: "M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z",
            }),
          ],
        );
      },
    },
  },
  {
    id: "batch",
    name: "批量检测",
    desc: "一次处理多张图片",
    icon: {
      render() {
        return h(
          "svg",
          { fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
          [
            h("path", {
              "stroke-linecap": "round",
              "stroke-linejoin": "round",
              "stroke-width": "2",
              d: "M12 6v6m0 0v6m0-6h6m-6 0H6",
            }),
          ],
        );
      },
    },
  },
];

const viewModes = [
  { id: "side", name: "并排对比" },
  { id: "grid", name: "栅格对比" },
];

const triggerUpload = () => {
  fileInput.value?.click();
};

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      uploadedImage.value = e.target?.result as string;
      detectionResult.value = null;
    };
    reader.readAsDataURL(file);
  }
};

const handleDrop = (e: DragEvent) => {
  dragOver.value = false;
  const file = e.dataTransfer?.files?.[0];
  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = (e) => {
      uploadedImage.value = e.target?.result as string;
      detectionResult.value = null;
    };
    reader.readAsDataURL(file);
  }
};

const startDetection = async () => {
  isDetecting.value = true;
  await new Promise((resolve) => setTimeout(resolve, 2000));
  detectionResult.value = {
    boxes: [
      {
        x: 20,
        y: 30,
        w: 15,
        h: 20,
        label: "裂纹",
        type: "表面缺陷",
        severity: "high",
        confidence: 0.95,
      },
      {
        x: 55,
        y: 45,
        w: 12,
        h: 18,
        label: "斑点",
        type: "表面状态",
        severity: "medium",
        confidence: 0.88,
      },
      {
        x: 70,
        y: 60,
        w: 10,
        h: 15,
        label: "划痕",
        type: "表面缺陷",
        severity: "low",
        confidence: 0.82,
      },
    ],
    time: 156,
  };
  isDetecting.value = false;
};

const resetDetection = () => {
  uploadedImage.value = undefined;
  detectionResult.value = null;
};
</script>
