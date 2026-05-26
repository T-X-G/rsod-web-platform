<template>
  <div
    class="relative overflow-hidden rounded-3xl border border-primary/20 bg-slate-950/70 shadow-[inset_0_0_30px_rgba(0,212,255,0.08)]"
  >
    <div
      class="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_top_left,rgba(0,212,255,0.12),transparent_30%)]"
    ></div>
    <div
      class="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-primary via-cyan-400 to-transparent opacity-80 animate-pulse"
    ></div>
    <div
      ref="viewer"
      class="relative h-full min-h-[420px] bg-[#08101f] overflow-hidden touch-none"
      @pointerdown="startDrag"
      @pointermove="onDrag"
      @pointerup="endDrag"
      @pointerleave="endDrag"
      @wheel.prevent="onWheel"
      @dblclick="resetZoom"
    >
      <div
        class="absolute inset-0 flex items-center justify-center overflow-hidden"
        :class="{ 'cursor-grab': zoom > 1, 'cursor-zoom-in': zoom === 1 }"
      >
        <img
          v-if="src"
          :src="src"
          :alt="alt"
          draggable="false"
          class="absolute max-w-none max-h-none object-contain select-none"
          :style="imageStyle"
        />
        <div
          v-else
          class="flex flex-col items-center justify-center h-full text-center px-6"
        >
          <div
            class="mb-4 w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center"
          >
            <svg
              class="w-8 h-8 text-primary"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
              />
            </svg>
          </div>
          <p class="text-white font-semibold">等待图片加载</p>
          <p class="text-sm text-gray-400">双击重置，滚轮缩放，拖拽移动</p>
        </div>
      </div>
      <div class="absolute inset-0 pointer-events-none">
        <slot name="overlay" />
      </div>
    </div>
    <div
      class="absolute bottom-4 left-4 right-4 flex items-center justify-between gap-3 text-xs text-gray-300"
    >
      <div
        class="flex items-center gap-2 bg-black/40 px-3 py-2 rounded-full backdrop-blur-sm"
      >
        <span class="font-medium text-white">缩放</span>
        <span>{{ zoom.toFixed(1) }}x</span>
      </div>
      <div
        class="flex items-center gap-2 bg-black/40 px-3 py-2 rounded-full backdrop-blur-sm"
      >
        <button
          type="button"
          @click="zoomOut"
          class="p-1 rounded-full bg-white/5 hover:bg-primary/20 transition-colors"
        >
          -
        </button>
        <button
          type="button"
          @click="zoomIn"
          class="p-1 rounded-full bg-white/5 hover:bg-primary/20 transition-colors"
        >
          +
        </button>
        <button
          type="button"
          @click="resetZoom"
          class="p-1 rounded-full bg-white/5 hover:bg-primary/20 transition-colors"
        >
          重置
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

defineProps({
  src: { type: String, default: "" },
  alt: { type: String, default: "Image preview" },
});

const zoom = ref(1);
const translateX = ref(0);
const translateY = ref(0);
const dragging = ref(false);
const startX = ref(0);
const startY = ref(0);
const offsetX = ref(0);
const offsetY = ref(0);
const viewer = ref<HTMLElement | null>(null);

const clamp = (value: number, min: number, max: number) =>
  Math.min(Math.max(value, min), max);

const imageStyle = computed(() => ({
  transform: `translate(-50%, -50%) translate(${translateX.value}px, ${translateY.value}px) scale(${zoom.value})`,
  left: "50%",
  top: "50%",
}));

const startDrag = (event: PointerEvent) => {
  if (zoom.value <= 1) return;
  dragging.value = true;
  startX.value = event.clientX;
  startY.value = event.clientY;
  offsetX.value = translateX.value;
  offsetY.value = translateY.value;

  const target = event.currentTarget as HTMLElement | null;
  if (target) {
    target.setPointerCapture(event.pointerId);
  }
};

const onDrag = (event: PointerEvent) => {
  if (!dragging.value) return;
  const dx = event.clientX - startX.value;
  const dy = event.clientY - startY.value;
  translateX.value = offsetX.value + dx;
  translateY.value = offsetY.value + dy;
};

const endDrag = () => {
  dragging.value = false;
};

const resetZoom = () => {
  zoom.value = 1;
  translateX.value = 0;
  translateY.value = 0;
};

const zoomIn = () => {
  zoom.value = clamp(zoom.value + 0.25, 1, 3);
};

const zoomOut = () => {
  zoom.value = clamp(zoom.value - 0.25, 1, 3);
};

const onWheel = (event: WheelEvent) => {
  const delta = event.deltaY > 0 ? -0.15 : 0.15;
  const nextZoom = clamp(zoom.value + delta, 1, 3);
  const rect = viewer.value?.getBoundingClientRect();

  if (rect) {
    const mouseX = event.clientX - rect.left - rect.width / 2;
    const mouseY = event.clientY - rect.top - rect.height / 2;
    const scaleFactor = nextZoom / zoom.value;
    translateX.value = mouseX - (mouseX - translateX.value) * scaleFactor;
    translateY.value = mouseY - (mouseY - translateY.value) * scaleFactor;
  }

  zoom.value = nextZoom;
};
</script>
