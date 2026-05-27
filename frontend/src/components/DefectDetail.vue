<template>
  <div class="space-y-8 animate-fadeIn">
    <!-- Header with Breadcrumb and Key Info -->
    <div>
      <div class="flex items-center gap-2 text-sm text-gray-500 mb-4">
        <span>缺陷库</span>
        <span class="text-gray-600">›</span>
        <span class="text-primary">{{ category }}</span>
        <span class="text-gray-600">›</span>
        <span class="text-white font-medium">{{ name }}</span>
      </div>

      <!-- Title Section with Badge -->
      <div class="flex items-start justify-between gap-6 mb-6 flex-wrap">
        <div>
          <h2 class="text-3xl font-bold text-white mb-2">{{ name }}</h2>
          <p class="text-base text-gray-400 italic">{{ englishName }}</p>
        </div>
        <div class="flex items-center gap-3">
          <span :class="['badge-primary px-4 py-2 text-sm font-medium']">{{
            priority
          }}</span>
          <div
            :class="[
              'px-4 py-2 rounded-lg text-sm font-semibold',
              riskLevelBadgeClass,
            ]"
          >
            {{ riskLevel }}级风险
          </div>
        </div>
      </div>

      <!-- Quick Description -->
      <div
        class="p-4 bg-gradient-to-r from-primary/10 via-cyan-500/10 to-primary/10 rounded-xl border border-primary/30"
      >
        <p class="text-base text-gray-200 leading-relaxed">{{ description }}</p>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
      <!-- Left Column: Basic Info + Gallery -->
      <div class="xl:col-span-2 space-y-8">
        <!-- Basic Information Panel -->
        <div>
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-6 bg-primary rounded-full" />
            <h3 class="text-lg font-bold text-white">基础信息</h3>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <div
              class="p-4 bg-white/5 rounded-xl border border-primary/20 hover:border-primary/50 transition-all"
            >
              <p class="text-xs text-gray-400 mb-2 uppercase">缺陷名称</p>
              <p class="text-base font-semibold text-white">{{ name }}</p>
            </div>
            <div
              class="p-4 bg-white/5 rounded-xl border border-primary/20 hover:border-primary/50 transition-all"
            >
              <p class="text-xs text-gray-400 mb-2 uppercase">英文名</p>
              <p class="text-base font-semibold text-primary">
                {{ englishName }}
              </p>
            </div>
            <div
              class="p-4 bg-white/5 rounded-xl border border-primary/20 hover:border-primary/50 transition-all"
            >
              <p class="text-xs text-gray-400 mb-2 uppercase">分类</p>
              <p class="text-base font-semibold text-cyan-400">
                {{ category }}
              </p>
            </div>
            <div
              class="p-4 bg-white/5 rounded-xl border border-primary/20 hover:border-primary/50 transition-all"
            >
              <p class="text-xs text-gray-400 mb-2 uppercase">优先级</p>
              <p class="text-base font-semibold text-orange-400">
                {{ priority }}
              </p>
            </div>
            <div
              class="p-4 bg-white/5 rounded-xl border border-primary/20 hover:border-primary/50 transition-all"
            >
              <p class="text-xs text-gray-400 mb-2 uppercase">风险等级</p>
              <p :class="['text-base font-semibold', riskLevelTextClass]">
                {{ riskLevel }}
              </p>
            </div>
            <div
              class="p-4 bg-white/5 rounded-xl border border-primary/20 hover:border-primary/50 transition-all"
            >
              <p class="text-xs text-gray-400 mb-2 uppercase">样本数</p>
              <p class="text-base font-semibold text-primary">
                {{ images.length }}
              </p>
            </div>
          </div>
        </div>

        <!-- Image Gallery -->
        <div>
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-6 bg-primary rounded-full" />
            <h3 class="text-lg font-bold text-white">示例图库</h3>
          </div>
          <div class="glass-card p-6">
            <DefectGallery :images="images" />
          </div>
        </div>
      </div>

      <!-- Right Column: Quick Reference -->
      <div class="space-y-6">
        <!-- Industrial Scenario -->
        <div class="glass-card p-6">
          <div class="flex items-center gap-2 mb-4">
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
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5.581m-5.419 0H3m2 0h5.581M9 7h.01M9 11h.01M9 15h.01M13 7h.01M13 11h.01M13 15h.01"
              />
            </svg>
            <h4 class="font-semibold text-white text-sm uppercase">工业场景</h4>
          </div>
          <p class="text-sm text-gray-300 leading-relaxed">
            {{ industrialScenario }}
          </p>
        </div>

        <!-- Detection Suggestions -->
        <div class="glass-card p-6">
          <div class="flex items-center gap-2 mb-4">
            <svg
              class="w-5 h-5 text-cyan-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <h4 class="font-semibold text-white text-sm uppercase">检测建议</h4>
          </div>
          <ul class="space-y-2">
            <li
              v-for="(suggestion, index) in detectionSuggestions"
              :key="index"
              class="flex gap-2 text-xs text-gray-300"
            >
              <span class="text-primary font-bold flex-shrink-0">•</span>
              <span>{{ suggestion }}</span>
            </li>
          </ul>
        </div>

        <!-- Impact Overview -->
        <div
          class="glass-card p-6 bg-gradient-to-b from-red-500/10 to-transparent border-red-500/30"
        >
          <div class="flex items-center gap-2 mb-4">
            <svg
              class="w-5 h-5 text-red-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4v2m0 4v2m0 4v.01M12 3a9 9 0 110 18 9 9 0 010-18z"
              />
            </svg>
            <h4 class="font-semibold text-white text-sm uppercase">影响速览</h4>
          </div>
          <ul class="space-y-2">
            <li
              v-for="(impact, index) in impactList"
              :key="index"
              class="flex gap-2 text-xs"
            >
              <span class="text-red-400 font-bold flex-shrink-0">!</span>
              <span class="text-gray-300">{{ impact }}</span>
            </li>
          </ul>
        </div>

        <!-- Quick Stats -->
        <div class="glass-card p-6 grid grid-cols-2 gap-3">
          <div
            class="p-3 bg-white/5 rounded-lg text-center border border-primary/10"
          >
            <p class="text-xs text-gray-400 mb-1">常见工序</p>
            <p class="text-lg font-bold text-primary">
              {{ commonProcesses.length }}
            </p>
          </div>
          <div
            class="p-3 bg-white/5 rounded-lg text-center border border-primary/10"
          >
            <p class="text-xs text-gray-400 mb-1">预防措施</p>
            <p class="text-lg font-bold text-cyan-400">
              {{ preventionMeasures.length }}
            </p>
          </div>
          <div
            class="p-3 bg-white/5 rounded-lg text-center border border-primary/10"
          >
            <p class="text-xs text-gray-400 mb-1">推荐模型</p>
            <p class="text-lg font-bold text-green-400">
              {{ recommendedModels.length }}
            </p>
          </div>
          <div
            class="p-3 bg-white/5 rounded-lg text-center border border-primary/10"
          >
            <p class="text-xs text-gray-400 mb-1">示例图片</p>
            <p class="text-lg font-bold text-orange-400">{{ images.length }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Risk Panel - Full Width -->
    <div>
      <div class="flex items-center gap-2 mb-6">
        <div class="w-1 h-6 bg-primary rounded-full" />
        <h3 class="text-xl font-bold text-white">详细风险评估</h3>
      </div>
      <div class="glass-card p-8">
        <RiskPanel
          :risk-level="riskLevel"
          :causes="causes"
          :impact="impactList"
          :performance-impact="performanceImpact"
          :common-processes="commonProcesses"
          :detection-difficulty="detectionDifficulty"
          :prevention-measures="preventionMeasures"
          :ai-detection-focus="aiDetectionFocus"
          :recommended-models="recommendedModels"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import DefectGallery from "./DefectGallery.vue";
import RiskPanel from "./RiskPanel.vue";
import type { DefectDetail } from "../data/defects.ts";

interface Props extends DefectDetail {}

const props = defineProps<Props>();

// Computed properties
const impactList = computed(() => props.impact);

const riskLevelBadgeClass = computed(() => {
  const classes = {
    低: "bg-green-500/20 text-green-400 border border-green-500/30",
    中: "bg-orange-500/20 text-orange-400 border border-orange-500/30",
    高: "bg-red-500/20 text-red-400 border border-red-500/30",
  };
  return classes[props.riskLevel];
});

const riskLevelTextClass = computed(() => {
  const classes = {
    低: "text-green-400",
    中: "text-orange-400",
    高: "text-red-400",
  };
  return classes[props.riskLevel];
});
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.5s ease-out;
}
</style>
