<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Particle {
  id: number
  x: number
  y: number
  size: number
  duration: number
  delay: number
  color: string
}

const particles = ref<Particle[]>([])

const colors = [
  'rgba(0, 212, 255, 0.6)',
  'rgba(6, 182, 212, 0.5)',
  'rgba(0, 212, 255, 0.4)',
  'rgba(255, 107, 53, 0.3)',
]

const generateParticles = () => {
  const newParticles: Particle[] = []
  for (let i = 0; i < 50; i++) {
    newParticles.push({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 2,
      duration: Math.random() * 20 + 15,
      delay: Math.random() * 20,
      color: colors[Math.floor(Math.random() * colors.length)]
    })
  }
  particles.value = newParticles
}

onMounted(() => {
  generateParticles()
})
</script>

<template>
  <div class="fixed inset-0 pointer-events-none overflow-hidden">
    <div
      v-for="particle in particles"
      :key="particle.id"
      class="absolute rounded-full opacity-60"
      :style="{
        left: `${particle.x}%`,
        top: `${particle.y}%`,
        width: `${particle.size}px`,
        height: `${particle.size}px`,
        background: particle.color,
        boxShadow: `0 0 ${particle.size * 2}px ${particle.color}`,
        animation: `particle ${particle.duration}s linear infinite`,
        animationDelay: `-${particle.delay}s`
      }"
    ></div>
  </div>
</template>
