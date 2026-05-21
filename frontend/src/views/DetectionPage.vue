<template>
  <div class="detection-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="breadcrumb">
        <span>工作台</span>
        <span class="separator">›</span>
        <span class="active">智能检测</span>
      </div>
      <h1 class="page-title">上传钢材表面图片，立即识别缺陷</h1>
      <p class="page-subtitle">
        支持裂纹 / 夹杂物 / 斑点 / 麻面 / 轧入氧化皮 / 划痕等缺陷检测
      </p>
    </div>

    <!-- 模型选择器 -->
    <div class="model-selector">
      <el-select v-model="selectedModel" style="width: 180px">
        <el-option label="rsod-yolo11n" value="rsod-yolo11n" />
      </el-select>
    </div>

    <!-- 功能选项卡 -->
    <div class="function-tabs">
      <div
        v-for="tab in functionTabs"
        :key="tab.key"
        class="function-tab"
        :class="{ active: activeTab === tab.key }"
        :data-key="tab.key"
        @click="handleTabClick(tab.key)"
      >
        <input
          type="file"
          :accept="tab.accept"
          :multiple="tab.multiple"
          class="file-input"
          @change="handleFileChange($event, tab.key)"
          @click.stop
          ref="fileInputs"
        />
        <el-icon :size="18" class="tab-icon"
          ><component :is="tab.icon"
        /></el-icon>
        <div class="tab-content">
          <span class="tab-text">{{ tab.name }}</span>
          <span class="tab-desc">{{ tab.desc }}</span>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧检测结果区域 -->
      <div class="left-panel">
        <div class="panel-header">
          <span class="panel-title">检测预览</span>
          <el-tag
            :type="hasImage && detectionResult ? 'success' : 'info'"
            effect="light"
            class="result-tag"
          >
            <el-icon class="el-icon--left" v-if="hasImage && detectionResult"
              ><Check
            /></el-icon>
            <el-icon class="el-icon--left" v-else><Upload /></el-icon>
            {{ hasImage && detectionResult ? "检测完成" : "等待上传" }}
          </el-tag>
        </div>

        <!-- 工具栏 -->
        <div class="toolbar">
          <el-button
            :class="{ active: compareMode === 'side' }"
            size="small"
            @click="compareMode = 'side'"
          >
            <el-icon><Minus /></el-icon>
            并排对比
          </el-button>
          <el-button
            :class="{ active: compareMode === 'grid' }"
            size="small"
            @click="compareMode = 'grid'"
          >
            <el-icon><Grid /></el-icon>
            栅格对比
          </el-button>
        </div>

        <!-- 图片对比区域 -->
        <div class="image-compare">
          <div class="image-card" @click="hasImage && originalImage && openImageViewer(originalImage, '原始图片')">
            <template v-if="hasImage && originalImage">
              <img :src="originalImage" alt="原始图片" class="compare-image" />
              <div class="image-overlay">
                <el-icon class="zoom-icon"><ZoomIn /></el-icon>
                <span class="overlay-text">点击放大查看</span>
              </div>
            </template>
            <template v-else>
              <div class="image-placeholder">
                <el-icon class="placeholder-icon"><Upload /></el-icon>
                <p class="placeholder-text">请上传图片</p>
                <p class="placeholder-desc">支持 jpg、png 格式</p>
              </div>
            </template>
            <div class="image-label">原始图片</div>
          </div>
          <div class="image-card" @click="hasImage && resultImage && openImageViewer(resultImage, '检测结果')">
            <template v-if="hasImage && resultImage">
              <img :src="resultImage" alt="检测结果" class="compare-image" />
              <div class="detection-mark" v-if="detectionResult"></div>
              <div class="image-overlay">
                <el-icon class="zoom-icon"><ZoomIn /></el-icon>
                <span class="overlay-text">点击放大查看</span>
              </div>
            </template>
            <template v-else>
              <div class="image-placeholder">
                <el-icon class="placeholder-icon"><View /></el-icon>
                <p class="placeholder-text">检测结果将在此展示</p>
                <p class="placeholder-desc">上传图片后开始检测</p>
              </div>
            </template>
            <div class="image-label">检测结果</div>
          </div>
        </div>
      </div>

      <!-- 模型信息 -->
      <div class="info-card">
        <div class="card-header">
          <el-icon><View /></el-icon>
          <span class="card-title">检测模型信息</span>
        </div>
        <div class="info-content">
          <div class="info-item">
            <span class="info-label">检测模型</span>
            <span class="info-value">{{ selectedModel }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">模型版本</span>
            <span class="info-value">v1.0.0</span>
          </div>
        </div>
      </div>

      <!-- 识别清单 -->
      <div class="result-card">
        <div class="card-header">
          <el-icon><List /></el-icon>
          <span class="card-title">识别清单</span>
        </div>
        <div v-if="!hasImage" class="empty-state">
          <el-icon class="empty-icon"><Upload /></el-icon>
          <p class="empty-text">请上传图片开始检测</p>
          <p class="empty-desc">上传钢材表面图片以识别缺陷</p>
        </div>
        <div
          v-else-if="!detectionResult || detectionResult.total_objects === 0"
          class="empty-state"
        >
          <el-icon class="empty-icon"><CircleCheck /></el-icon>
          <p class="empty-text">未检测到目标</p>
          <p class="empty-desc">影像无异常目标</p>
        </div>
        <div v-else class="detection-list">
          <div
            v-for="(box, index) in detectionResult.boxes"
            :key="index"
            class="detection-item"
          >
            <span class="item-name">{{ box.class_name }}</span>
            <span class="item-confidence"
              >{{ (box.confidence * 100).toFixed(1) }}%</span
            >
          </div>
        </div>
      </div>

      <!-- AI诊断建议 -->
      <div class="result-card">
        <div class="card-header">
          <el-icon><ChatDotRound /></el-icon>
          <span class="card-title">AI 诊断建议</span>
        </div>
        <div class="diagnosis-content">
          <p v-if="!hasImage">上传图片后将自动生成诊断建议</p>
          <p v-else-if="!detectionResult">未检测到指定目标</p>
          <p v-else>
            检测到 {{ detectionResult.total_objects }} 个目标，耗时
            {{ detectionResult.detection_time }}s。 模型:
            {{ detectionResult.model_name }}
          </p>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-card">
        <div class="action-buttons">
          <el-button
            size="default"
            class="btn-secondary"
            @click="handleRedetect"
          >
            <el-icon><Refresh /></el-icon>
            重新检测
          </el-button>
          <el-button type="primary" size="default" class="btn-primary">
            查看完整报告
          </el-button>
        </div>
      </div>
    </div>

    <!-- 图片查看器弹窗 -->
    <Teleport to="body">
      <div
        v-if="showImageViewer"
        class="image-viewer-overlay"
        @click="closeImageViewer"
      >
        <div class="image-viewer">
          <div class="viewer-header">
            <span class="viewer-title">{{ viewerTitle }}</span>
            <div class="viewer-controls">
              <el-button size="small" @click.stop="zoomOut">
                <el-icon><ZoomOut /></el-icon>
              </el-button>
              <span class="zoom-value">{{ Math.round(imageScale * 100) }}%</span>
              <el-button size="small" @click.stop="zoomIn">
                <el-icon><ZoomIn /></el-icon>
              </el-button>
              <el-button size="small" @click.stop="resetZoom">
                重置
              </el-button>
              <el-button size="small" @click.stop="closeImageViewer">
                <el-icon><Close /></el-icon>
              </el-button>
            </div>
          </div>
          <div
            class="viewer-content"
            @mousedown="handleMouseDown"
            @mousemove="handleMouseMove"
            @mouseup="handleMouseUp"
            @mouseleave="handleMouseUp"
            @wheel="handleWheel"
          >
            <img
              :src="viewerImageUrl"
              :alt="viewerTitle"
              class="viewer-image"
              :style="{
                transform: `scale(${imageScale}) translate(${imageOffsetX / imageScale}px, ${imageOffsetY / imageScale}px)`,
                cursor: imageScale > 1 ? 'grab' : 'default'
              }"
            />
          </div>
          <div class="viewer-hint">
            <span>滚轮缩放</span>
            <span>|</span>
            <span>拖拽平移</span>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage, ElLoading } from "element-plus";
import {
  Picture,
  Plus,
  Check,
  Grid,
  List,
  CircleCheck,
  ChatDotRound,
  Refresh,
  Minus,
  Upload,
  View,
  Close,
  ZoomIn,
  ZoomOut,
} from "@element-plus/icons-vue";
import { detectSingleImage } from "../api/detection";

const selectedModel = ref("rsod-yolo11n");
const activeTab = ref("single");
const compareMode = ref("side");
const originalImage = ref(null);
const resultImage = ref(null);
const detectionResult = ref(null);
const isDetecting = ref(false);
const hasImage = ref(false);

// 图片查看器状态
const showImageViewer = ref(false);
const viewerImageUrl = ref("");
const viewerTitle = ref("");
const imageScale = ref(1);
const imageOffsetX = ref(0);
const imageOffsetY = ref(0);
const isDragging = ref(false);
const dragStartX = ref(0);
const dragStartY = ref(0);

const openImageViewer = (url, title) => {
  viewerImageUrl.value = url;
  viewerTitle.value = title;
  imageScale.value = 1;
  imageOffsetX.value = 0;
  imageOffsetY.value = 0;
  showImageViewer.value = true;
};

const closeImageViewer = () => {
  showImageViewer.value = false;
};

const zoomIn = () => {
  imageScale.value = Math.min(imageScale.value + 0.25, 4);
};

const zoomOut = () => {
  imageScale.value = Math.max(imageScale.value - 0.25, 0.25);
};

const resetZoom = () => {
  imageScale.value = 1;
  imageOffsetX.value = 0;
  imageOffsetY.value = 0;
};

const handleMouseDown = (e) => {
  if (imageScale.value > 1) {
    isDragging.value = true;
    dragStartX.value = e.clientX - imageOffsetX.value;
    dragStartY.value = e.clientY - imageOffsetY.value;
  }
};

const handleMouseMove = (e) => {
  if (isDragging.value) {
    imageOffsetX.value = e.clientX - dragStartX.value;
    imageOffsetY.value = e.clientY - dragStartY.value;
  }
};

const handleMouseUp = () => {
  isDragging.value = false;
};

const handleWheel = (e) => {
  e.preventDefault();
  const delta = e.deltaY > 0 ? -0.1 : 0.1;
  imageScale.value = Math.max(0.25, Math.min(imageScale.value + delta, 4));
};

const functionTabs = [
  {
    key: "single",
    name: "单图检测",
    desc: "快速识别一张图片",
    icon: Picture,
    accept: "image/*",
    multiple: false,
  },
  {
    key: "batch",
    name: "批量检测",
    desc: "一次处理多张图片",
    icon: Plus,
    accept: "image/*",
    multiple: true,
  },
];

const fileInputs = ref([]);

const handleTabClick = (key) => {
  activeTab.value = key;
  const input = document.querySelector(
    `.function-tab[data-key="${key}"] .file-input`, //.function-tab data-key="single" .file-inputsingle
  );
  if (input) {
    input.click();
  }
};

const handleFileChange = async (event, tabKey) => {
  event.stopPropagation();
  event.preventDefault();
  const files = event.target.files;
  if (files && files.length > 0) {
    if (tabKey === "single") {
      await performSingleDetection(files[0]);
    }
  }
  setTimeout(() => {
    event.target.value = "";
  }, 0);
};

const performSingleDetection = async (file) => {
  const loading = ElLoading.service({
    lock: true,
    text: "正在检测中...",
    background: "rgba(0, 0, 0, 0.7)",
  });

  try {
    isDetecting.value = true;
    hasImage.value = true;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("model_name", selectedModel.value);

    originalImage.value = URL.createObjectURL(file);

    const response = await detectSingleImage(formData);
    if (response.success && response.data) {
      detectionResult.value = response.data;
      resultImage.value = response.data.result_image_url;
      ElMessage.success("检测成功！");
    } else {
      ElMessage.error(response.message || "检测失败");
    }
  } catch (error) {
    console.error("检测错误:", error);
    ElMessage.error("检测失败，请稍后重试");
  } finally {
    isDetecting.value = false;
    loading.close();
  }
};

const handleRedetect = () => {
  const input = document.querySelector(
    `.function-tab[data-key="single"] .file-input`,
  );
  if (input) {
    input.click();
  }
};
</script>

<style scoped>
.detection-page {
  width: 100%;
  position: relative;
}

.page-header {
  margin-bottom: var(--spacing-xl);
  padding-top: 0;
}

.breadcrumb {
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin-bottom: var(--spacing-sm);
}

.separator {
  margin: 0 6px;
}

.breadcrumb .active {
  color: var(--text-primary);
  font-weight: 500;
}

.page-title {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.page-subtitle {
  font-size: var(--text-base);
  color: var(--text-secondary);
}

.model-selector {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 10;
}

.model-selector .el-select {
  border-radius: var(--radius-md);
  border-color: var(--border-color);
}

/* 功能选项卡 */
.function-tabs {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
  justify-content: center;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.function-tab {
  flex: 1;
  min-width: 200px;
  max-width: 280px;
  display: flex;
  align-items: center;
  padding: var(--spacing-lg);
  background-color: var(--bg-card);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.file-input {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 10;
}

.function-tab:hover {
  background-color: var(--primary-light);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.function-tab.active {
  background-color: var(--primary-light);
  border-color: var(--primary-color);
  box-shadow: var(--shadow-md);
}

.tab-icon {
  font-size: 24px;
  color: var(--primary-color);
  margin-right: var(--spacing-md);
  flex-shrink: 0;
}

.tab-content {
  display: flex;
  flex-direction: column;
}

.tab-text {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
}

.tab-desc {
  font-size: var(--text-xs);
  color: var(--text-muted);
  line-height: 1.4;
}

/* 主内容区域 */
.main-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* 检测预览面板 */
.left-panel {
  background-color: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-lg);
}

.panel-title {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.result-tag {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: var(--text-xs);
}

.toolbar {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
}

.toolbar .el-button {
  border-radius: var(--radius-md);
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: var(--text-sm);
}

.toolbar .el-button.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
  border-color: var(--primary-color);
}

/* 图片对比区域 */
.image-compare {
  display: flex;
  gap: var(--spacing-lg);
  height: 360px;
}

.image-card {
  flex: 1;
  position: relative;
  border-radius: var(--radius-md);
  overflow: hidden;
  background-color: var(--bg-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.image-card:hover {
  box-shadow: var(--shadow-md);
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  padding: var(--spacing-lg);
  text-align: center;
}

.placeholder-icon {
  font-size: 56px;
  color: var(--text-light);
  margin-bottom: var(--spacing-md);
}

.placeholder-text {
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xs);
}

.placeholder-desc {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.compare-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all var(--transition-normal);
  pointer-events: none;
}

.image-card:hover .image-overlay {
  background: rgba(0, 0, 0, 0.4);
  opacity: 1;
}

.zoom-icon {
  font-size: 32px;
  color: white;
  margin-bottom: var(--spacing-xs);
}

.overlay-text {
  font-size: var(--text-sm);
  color: white;
}

.image-label {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--spacing-sm) var(--spacing-md);
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: var(--text-sm);
}

.detection-mark {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-md);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.detection-mark::after {
  content: "✓";
  color: white;
  font-size: 20px;
  font-weight: bold;
}

/* 信息卡片 */
.info-card {
  background-color: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.card-header .el-icon {
  font-size: var(--text-lg);
  color: var(--primary-color);
  margin-right: var(--spacing-sm);
}

.card-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
}

.info-content {
  display: flex;
  gap: var(--spacing-xl);
}

.info-item {
  flex: 1;
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--border-light);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.info-value {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
}

/* 结果卡片 */
.result-card {
  background-color: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-xl) 0;
}

.empty-icon {
  font-size: 56px;
  color: var(--success-color);
  margin-bottom: var(--spacing-md);
}

.empty-text {
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.empty-desc {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.diagnosis-content {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.8;
  padding: var(--spacing-sm) 0;
}

.detection-list {
  max-height: 240px;
  overflow-y: auto;
}

.detection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--bg-secondary);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-sm);
  transition: all var(--transition-fast);
}

.detection-item:hover {
  background-color: var(--primary-light);
}

.detection-item:last-child {
  margin-bottom: 0;
}

.item-name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.item-confidence {
  font-size: var(--text-sm);
  color: var(--primary-color);
  font-weight: 600;
}

/* 操作按钮卡片 */
.action-card {
  background-color: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
}

.btn-secondary {
  flex: 1;
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  font-size: var(--text-sm);
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background-color: var(--bg-hover);
  border-color: var(--border-color);
}

.btn-primary {
  flex: 2;
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  font-size: var(--text-sm);
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  border-color: var(--primary-dark);
}

/* 图片查看器 */
.image-viewer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 1;
  transition: opacity var(--transition-fast);
}

.image-viewer {
  width: 90%;
  max-width: 1200px;
  height: 90vh;
  background: #1a1a1a;
  border-radius: var(--radius-xl);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  background: #2a2a2a;
  border-bottom: 1px solid #3a3a3a;
}

.viewer-title {
  font-size: var(--text-sm);
  color: white;
  font-weight: 500;
}

.viewer-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.zoom-value {
  font-size: var(--text-xs);
  color: var(--text-muted);
  min-width: 50px;
  text-align: center;
}

.viewer-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  overflow: hidden;
  background: #0a0a0a;
}

.viewer-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform var(--transition-fast);
}

.viewer-image:active {
  cursor: grabbing;
}

.viewer-hint {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
  background: #2a2a2a;
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.viewer-hint span {
  display: flex;
  align-items: center;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .function-tabs {
    flex-direction: column;
    align-items: center;
    max-width: 100%;
  }

  .function-tab {
    width: 100%;
    max-width: none;
  }

  .image-compare {
    flex-direction: column;
    height: auto;
  }

  .image-card {
    height: 240px;
  }

  .info-content {
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-secondary,
  .btn-primary {
    flex: none;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: var(--text-2xl);
  }

  .image-card {
    height: 200px;
  }

  .left-panel,
  .info-card,
  .result-card,
  .action-card {
    padding: var(--spacing-md);
  }
}
</style>
