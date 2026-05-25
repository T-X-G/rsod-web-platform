<template>
  <div class="absolute inset-0 pointer-events-none">
    <div
      class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.04),transparent_30%)]"
    ></div>
    <div class="absolute inset-0 opacity-80">
      <div
        class="scanner-line absolute left-0 w-full h-0.5 bg-cyan-400/60 blur-sm"
      />
    </div>
    <div
      v-for="(box, index) in boxes"
      :key="index"
      class="absolute rounded-2xl border-2 shadow-[0_0_20px_rgba(0,212,255,0.14)]"
      :style="getBoxStyle(box)"
    >
      <div
        class="absolute -top-5 left-0 rounded-br-2xl px-2 py-1 text-[11px] font-semibold text-white"
        :style="{ backgroundColor: box.color }"
      >
        {{ box.label }} {{ (box.confidence * 100).toFixed(0) }}%
      </div>
      <div class="absolute inset-0 border border-white/20 rounded-2xl"></div>
      <div
        class="absolute inset-0 bg-gradient-to-br from-white/10 via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DetectionBox } from "../mock/detection";

defineProps({
  boxes: { type: Array as () => DetectionBox[], default: () => [] },
});

const getBoxStyle = (box: DetectionBox) => {
  return {
    left: `${box.bbox[0]}%`,
    top: `${box.bbox[1]}%`,
    width: `${box.bbox[2]}%`,
    height: `${box.bbox[3]}%`,
    boxShadow: `0 0 18px ${box.color}80`,
    borderColor: box.color,
  };
};
</script>
