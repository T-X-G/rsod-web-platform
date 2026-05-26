<script setup lang="ts">
// Logo icon component
</script>

<template>
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" class="text-primary">
    <!-- Outer hexagon -->
    <path
      d="M24 4L42 14V34L24 44L6 34V14L24 4Z"
      stroke="currentColor"
      stroke-width="2"
      fill="none"
      class="opacity-30"
    />
    
    <!-- Inner hexagon -->
    <path
      d="M24 10L36 17V31L24 38L12 31V17L24 10Z"
      stroke="currentColor"
      stroke-width="2"
      fill="none"
      class="opacity-60"
    />
    
    <!-- Center eye/scan element -->
    <circle
      cx="24"
      cy="24"
      r="6"
      stroke="currentColor"
      stroke-width="2"
      fill="none"
    />
    <circle
      cx="24"
      cy="24"
      r="2"
      fill="currentColor"
    />
    
    <!-- Scan lines -->
    <line
      x1="24"
      y1="14"
      x2="24"
      y2="18"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
    />
    <line
      x1="24"
      y1="30"
      x2="24"
      y2="34"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
    />
    <line
      x1="14"
      y1="24"
      x2="18"
      y2="24"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
    />
    <line
      x1="30"
      y1="24"
      x2="34"
      y2="24"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
    />
    
    <!-- Corner accents -->
    <path
      d="M10 10L14 14"
      stroke="url(#gradient)"
      stroke-width="2"
      stroke-linecap="round"
    />
    <path
      d="M38 10L34 14"
      stroke="url(#gradient)"
      stroke-width="2"
      stroke-linecap="round"
    />
    <path
      d="M10 38L14 34"
      stroke="url(#gradient)"
      stroke-width="2"
      stroke-linecap="round"
    />
    <path
      d="M38 38L34 34"
      stroke="url(#gradient)"
      stroke-width="2"
      stroke-linecap="round"
    />
    
    <defs>
      <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#00d4ff" />
        <stop offset="100%" stop-color="#ff6b35" />
      </linearGradient>
    </defs>
  </svg>
</template>
