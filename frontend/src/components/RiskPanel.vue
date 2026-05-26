<template>
  <div class="space-y-6">
    <!-- Risk Level Badge -->
    <div
      class="flex items-center gap-4 p-4 bg-white/5 rounded-xl border border-primary/20"
    >
      <div
        :class="[
          'w-14 h-14 rounded-lg flex items-center justify-center font-bold text-lg transition-all',
          riskLevelConfig.bgColor,
          riskLevelConfig.textColor,
        ]"
      >
        {{ riskLevel }}
      </div>
      <div>
        <p class="text-white font-semibold">风险等级评估</p>
        <p class="text-sm text-gray-400 mt-1">
          {{ riskLevelConfig.description }}
        </p>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Left Column -->
      <div class="space-y-6">
        <!-- Processes -->
        <div>
          <div class="flex items-center gap-2 mb-3">
            <div class="w-1 h-5 bg-primary rounded-full" />
            <h3
              class="text-sm font-semibold text-white uppercase tracking-wide"
            >
              常见工序
            </h3>
          </div>
          <div class="space-y-2">
            <div
              v-for="process in commonProcesses"
              :key="process"
              class="flex items-start gap-3 p-3 bg-white/5 rounded-lg border border-primary/10 hover:border-primary/30 hover:bg-white/10 transition-all"
            >
              <svg
                class="w-4 h-4 text-primary flex-shrink-0 mt-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
              <span class="text-sm text-gray-300">{{ process }}</span>
            </div>
          </div>
        </div>

        <!-- Detection Difficulty -->
        <div>
          <div class="flex items-center gap-2 mb-3">
            <div class="w-1 h-5 bg-orange-500 rounded-full" />
            <h3
              class="text-sm font-semibold text-white uppercase tracking-wide"
            >
              检测难点
            </h3>
          </div>
          <div
            class="p-4 bg-orange-500/10 rounded-xl border border-orange-500/30"
          >
            <p class="text-sm text-orange-200 leading-relaxed">
              {{ detectionDifficulty }}
            </p>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="space-y-6">
        <!-- Causes -->
        <div>
          <div class="flex items-center gap-2 mb-3">
            <div class="w-1 h-5 bg-red-500 rounded-full" />
            <h3
              class="text-sm font-semibold text-white uppercase tracking-wide"
            >
              产生原因
            </h3>
          </div>
          <div
            class="space-y-2 max-h-[200px] overflow-y-auto pr-2 custom-scrollbar"
          >
            <div
              v-for="cause in causes"
              :key="cause"
              class="flex items-start gap-3 p-3 bg-red-500/10 rounded-lg border border-red-500/20"
            >
              <svg
                class="w-4 h-4 text-red-400 flex-shrink-0 mt-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span class="text-sm text-gray-300">{{ cause }}</span>
            </div>
          </div>
        </div>

        <!-- AI Detection Focus -->
        <div>
          <div class="flex items-center gap-2 mb-3">
            <div class="w-1 h-5 bg-cyan-500 rounded-full" />
            <h3
              class="text-sm font-semibold text-white uppercase tracking-wide"
            >
              AI检测重点
            </h3>
          </div>
          <div class="p-4 bg-cyan-500/10 rounded-xl border border-cyan-500/30">
            <p class="text-sm text-cyan-200 leading-relaxed">
              {{ aiDetectionFocus }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Impact -->
    <div>
      <div class="flex items-center gap-2 mb-3">
        <div class="w-1 h-5 bg-yellow-500 rounded-full" />
        <h3 class="text-sm font-semibold text-white uppercase tracking-wide">
          性能影响分析
        </h3>
      </div>
      <div class="p-4 bg-yellow-500/10 rounded-xl border border-yellow-500/20">
        <p class="text-sm text-yellow-200 leading-relaxed">
          {{ performanceImpact }}
        </p>
      </div>
    </div>

    <!-- Prevention Measures -->
    <div>
      <div class="flex items-center gap-2 mb-3">
        <div class="w-1 h-5 bg-green-500 rounded-full" />
        <h3 class="text-sm font-semibold text-white uppercase tracking-wide">
          预防措施
        </h3>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div
          v-for="(measure, index) in preventionMeasures"
          :key="index"
          class="flex items-start gap-3 p-3 bg-green-500/10 rounded-lg border border-green-500/20 hover:border-green-500/50 hover:bg-green-500/20 transition-all"
        >
          <div
            class="w-6 h-6 rounded-full bg-green-500/30 text-green-400 flex items-center justify-center flex-shrink-0 text-xs font-semibold"
          >
            {{ index + 1 }}
          </div>
          <span class="text-sm text-gray-300">{{ measure }}</span>
        </div>
      </div>
    </div>

    <!-- Recommended Models -->
    <div>
      <div class="flex items-center gap-2 mb-3">
        <div class="w-1 h-5 bg-purple-500 rounded-full" />
        <h3 class="text-sm font-semibold text-white uppercase tracking-wide">
          推荐检测模型
        </h3>
      </div>
      <div class="space-y-2">
        <div
          v-for="model in recommendedModels"
          :key="model"
          class="flex items-center gap-3 p-3 bg-purple-500/10 rounded-lg border border-purple-500/20"
        >
          <div class="w-2 h-2 rounded-full bg-purple-400 flex-shrink-0" />
          <div>
            <p class="text-sm text-purple-200">{{ model }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Impact Summary -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
      <div
        v-for="(impact, index) in impacts"
        :key="index"
        class="p-3 bg-white/5 rounded-lg border border-primary/20 text-center hover:border-primary/50 hover:bg-primary/10 transition-all"
      >
        <p class="text-xs text-gray-400 mb-1">{{ impact.label }}</p>
        <p class="text-lg font-bold text-primary">{{ impact.value }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  riskLevel: "低" | "中" | "高";
  causes: string[];
  impact: string[];
  performanceImpact: string;
  commonProcesses: string[];
  detectionDifficulty: string;
  preventionMeasures: string[];
  aiDetectionFocus: string;
  recommendedModels: string[];
}

const props = defineProps<Props>();

const riskLevelConfig = computed(() => {
  const configs = {
    低: {
      bgColor: "bg-green-500/20",
      textColor: "text-green-400",
      description: "风险较低，但需要重点监控",
    },
    中: {
      bgColor: "bg-orange-500/20",
      textColor: "text-orange-400",
      description: "风险中等，需要严格控制工艺参数",
    },
    高: {
      bgColor: "bg-red-500/20",
      textColor: "text-red-400",
      description: "高风险缺陷，严禁存在于产品中",
    },
  };

  return configs[props.riskLevel];
});

const impacts = computed(() => [
  {
    label: "疲劳强度",
    value:
      props.riskLevel === "高"
        ? "↓30-50%"
        : props.riskLevel === "中"
          ? "↓15-20%"
          : "↓5-10%",
  },
  {
    label: "冲击韧性",
    value:
      props.riskLevel === "高"
        ? "↓30-40%"
        : props.riskLevel === "中"
          ? "↓15-20%"
          : "↓5%",
  },
  {
    label: "防腐能力",
    value:
      props.riskLevel === "高"
        ? "严重"
        : props.riskLevel === "中"
          ? "中等"
          : "轻微",
  },
  {
    label: "可用性",
    value:
      props.riskLevel === "高"
        ? "报废"
        : props.riskLevel === "中"
          ? "限制"
          : "可用",
  },
]);
</script>

<style scoped>
/* Custom scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(34, 211, 238, 0.3);
  border-radius: 2px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(34, 211, 238, 0.6);
}
</style>
