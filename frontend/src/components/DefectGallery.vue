<template>
  <div class="space-y-4">
    <!-- Main Image Display -->
    <div
      class="relative overflow-hidden rounded-2xl border border-primary/30 bg-white/5 aspect-video group"
    >
      <!-- Image Container -->
      <div class="relative w-full h-full overflow-hidden">
        <img
          :src="currentImage.url"
          :alt="`Defect image ${currentImageIndex + 1}`"
          class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <!-- Placeholder for missing images -->
        <div
          v-if="!currentImage.url || currentImage.url.includes('undefined')"
          class="absolute inset-0 bg-gradient-to-br from-primary/20 to-cyan-500/20 flex items-center justify-center"
        >
          <div class="text-center">
            <svg
              class="w-16 h-16 text-primary/40 mx-auto mb-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <div class="text-sm text-gray-500">示例图片</div>
            <div class="text-xs text-gray-600 mt-1">
              {{ currentImageIndex + 1 }}
            </div>
          </div>
        </div>
      </div>

      <!-- Image Caption and Navigation -->
      <div
        class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent p-4 pt-8"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-white font-medium text-sm">
              示例图片 {{ currentImageIndex + 1 }}
            </p>
            <p class="text-gray-300 text-xs mt-1">点击下方缩略图快速切换</p>
          </div>
          <div class="text-xs text-gray-400 whitespace-nowrap ml-4">
            {{ currentImageIndex + 1 }} / {{ images.length }}
          </div>
        </div>
      </div>

      <!-- Navigation Arrows -->
      <button
        @click="prevImage"
        class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/50 text-white hover:bg-primary/80 transition-all z-10 flex items-center justify-center group/btn opacity-0 group-hover:opacity-100"
        aria-label="Previous image"
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
            d="M15 19l-7-7 7-7"
          />
        </svg>
      </button>

      <button
        @click="nextImage"
        class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/50 text-white hover:bg-primary/80 transition-all z-10 flex items-center justify-center group/btn opacity-0 group-hover:opacity-100"
        aria-label="Next image"
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
            d="M9 5l7 7-7 7"
          />
        </svg>
      </button>

      <!-- Expand Button -->
      <button
        @click="showLightbox = true"
        class="absolute top-4 right-4 w-10 h-10 rounded-full bg-black/50 text-white hover:bg-primary/80 transition-all z-10 flex items-center justify-center opacity-0 group-hover:opacity-100"
        aria-label="Expand image"
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
            d="M10 6H6v4m12 0h4v-4m0 12h-4v4m4-4v4h4m-18-4h4v4H4m16-8V6m0 0H6m12 0v4"
          />
        </svg>
      </button>
    </div>

    <!-- Image Info and Actions -->
    <div class="flex items-center justify-between gap-4">
      <div class="text-xs text-gray-400">
        <span class="text-primary font-medium"
          >示例图片 {{ currentImageIndex + 1 }}</span
        >
      </div>
      <!-- Indicator dots for quick navigation -->
      <div class="flex gap-1">
        <button
          v-for="(img, index) in images"
          :key="img.id"
          @click="currentImageIndex = index"
          :class="[
            'w-2 h-2 rounded-full transition-all',
            index === currentImageIndex
              ? 'bg-primary w-6'
              : 'bg-white/20 hover:bg-white/40',
          ]"
          :aria-label="`Go to image ${index + 1}`"
        />
      </div>
    </div>

    <!-- Thumbnail Gallery -->
    <div class="space-y-2">
      <p class="text-xs text-gray-400 uppercase tracking-wide">缩略图</p>
      <div
        class="grid grid-cols-5 gap-2 max-h-[120px] overflow-y-auto pr-2 custom-scrollbar"
      >
        <button
          v-for="(image, index) in images"
          :key="image.id"
          @click="currentImageIndex = index"
          :class="[
            'relative rounded-lg overflow-hidden border-2 transition-all aspect-square group',
            index === currentImageIndex
              ? 'border-primary ring-2 ring-primary/50'
              : 'border-primary/20 hover:border-primary/50',
          ]"
          :title="`图片 ${index + 1}`"
        >
          <!-- Thumbnail Image -->
          <img
            :src="image.url"
            :alt="`图片 ${index + 1}`"
            class="w-full h-full object-cover group-hover:scale-110 transition-transform"
          />

          <!-- Placeholder -->
          <div
            v-if="!image.url || image.url.includes('undefined')"
            class="absolute inset-0 bg-gradient-to-br from-primary/30 to-cyan-500/30 flex items-center justify-center"
          >
            <svg
              class="w-5 h-5 text-primary/60"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          </div>

          <!-- Index Label -->
          <div
            class="absolute bottom-1 right-1 bg-black/60 text-white text-xs rounded px-2 py-0.5 group-hover:bg-primary/80 transition-colors"
          >
            {{ index + 1 }}
          </div>
        </button>
      </div>
    </div>

    <!-- Lightbox Modal -->
    <Teleport to="body" v-if="showLightbox">
      <div
        class="fixed inset-0 z-50 bg-black/95 flex items-center justify-center"
        @click="showLightbox = false"
      >
        <div
          class="relative w-full h-full flex items-center justify-center p-8"
          @click.stop
        >
          <!-- Close Button -->
          <button
            @click="showLightbox = false"
            class="absolute top-6 right-6 w-12 h-12 rounded-full bg-white/10 hover:bg-primary/80 text-white flex items-center justify-center transition-all z-10"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          <!-- Fullscreen Image -->
          <div
            class="relative max-w-4xl w-full h-full flex items-center justify-center"
          >
            <img
              :src="currentImage.url"
              :alt="`Defect image ${currentImageIndex + 1}`"
              class="max-w-full max-h-full object-contain"
            />

            <!-- Image Info in Fullscreen -->
            <div
              class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 to-transparent p-6"
            >
              <p class="text-white font-semibold text-lg">
                示例图片 {{ currentImageIndex + 1 }}
              </p>
              <p class="text-gray-300 text-sm mt-2">
                共 {{ images.length }} 张示例图
              </p>
              <p class="text-gray-400 text-xs mt-3">
                {{ currentImageIndex + 1 }} / {{ images.length }}
              </p>
            </div>

            <!-- Navigation in Fullscreen -->
            <button
              @click.stop="prevImage"
              class="absolute left-6 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 hover:bg-primary/80 text-white flex items-center justify-center transition-all"
            >
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </button>

            <button
              @click.stop="nextImage"
              class="absolute right-6 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 hover:bg-primary/80 text-white flex items-center justify-center transition-all"
            >
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import type { DefectImage } from "../data/defects";

interface Props {
  images: DefectImage[];
}

const props = withDefaults(defineProps<Props>(), {
  images: () => [],
});

const currentImageIndex = ref(0);
const showLightbox = ref(false);

const currentImage = computed(() => {
  return props.images[currentImageIndex.value] || { id: 0, url: "" };
});

const nextImage = () => {
  if (!props.images.length) return;
  currentImageIndex.value = (currentImageIndex.value + 1) % props.images.length;
};

const prevImage = () => {
  if (!props.images.length) return;
  currentImageIndex.value =
    (currentImageIndex.value - 1 + props.images.length) % props.images.length;
};
</script>

<style scoped>
/* Custom scrollbar for thumbnail gallery */
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
