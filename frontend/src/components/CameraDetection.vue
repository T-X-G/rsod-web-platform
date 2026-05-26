<template>
  <DashboardLayout>
    <div class="space-y-6">
      <div>
        <h1 class="text-2xl font-bold text-white mb-2">摄像头实时检测</h1>
        <p class="text-gray-400">实时画面 + 检测框可视化</p>
      </div>

      <div class="glass-card p-6 space-y-4">
        <!-- Controls -->
        <div class="flex items-center gap-3 flex-wrap">
          <button @click="startCamera" :disabled="stream !== null"
            class="px-5 py-2.5 bg-gradient-to-r from-primary to-cyan-400 text-white rounded-xl font-medium text-sm hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all">
            {{ stream ? '摄像头已开启' : '开启摄像头' }}
          </button>
          <button @click="togglePause" :disabled="!stream"
            class="px-5 py-2.5 border border-primary/30 rounded-xl font-medium text-sm transition-all"
            :class="isPaused ? 'text-green-400 border-green-400/30 hover:bg-green-400/10' : 'text-yellow-400 border-yellow-400/30 hover:bg-yellow-400/10'">
            {{ isPaused ? '恢复' : '暂停' }}
          </button>
          <button @click="stopCamera" :disabled="!stream"
            class="px-5 py-2.5 border border-red-500/20 text-red-400 rounded-xl font-medium text-sm hover:bg-red-500/10 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
            关闭摄像头
          </button>
          <div class="ml-auto flex items-center gap-4 text-sm">
            <span class="text-gray-400">FPS: <span class="text-primary font-medium">{{ fps }}</span></span>
            <span class="text-gray-400">检测: <span class="text-green-400 font-medium">{{ detectionCount }}</span></span>
            <span class="text-gray-400">耗时: <span class="text-yellow-400 font-medium">{{ lastDetectionTime }}ms</span></span>
          </div>
        </div>

        <!-- Camera View -->
        <div class="relative bg-black rounded-2xl overflow-hidden" style="min-height: 400px;">
          <video ref="videoRef" autoplay playsinline muted
            class="w-full h-full object-contain" style="max-height: 480px;" />
          <canvas ref="canvasRef"
            class="absolute inset-0 w-full h-full object-contain pointer-events-none" />
          <div v-if="!stream"
            class="absolute inset-0 flex items-center justify-center text-gray-500">
            <div class="text-center space-y-2">
              <svg class="w-12 h-12 mx-auto opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <p class="text-sm">点击"开启摄像头"开始</p>
            </div>
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="errorMsg"
          class="px-4 py-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm">
          {{ errorMsg }}
        </div>

        <!-- Detected Objects -->
        <div v-if="boxes.length > 0" class="space-y-2">
          <h3 class="text-sm font-medium text-gray-300">检测目标 ({{ boxes.length }})</h3>
          <div class="flex gap-2 flex-wrap">
            <span v-for="(box, i) in boxes" :key="i"
              class="px-3 py-1.5 rounded-full text-xs font-medium border"
              :class="getTagClass(box)">
              {{ box.chinese_name || box.class_name }} {{ (box.confidence * 100).toFixed(0) }}%
            </span>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from "vue"
import DashboardLayout from "../layouts/DashboardLayout.vue"

interface DetectionBox {
  x1: number; y1: number; x2: number; y2: number
  confidence: number; class_name: string; chinese_name: string
}

const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const stream = ref<MediaStream | null>(null)
const isPaused = ref(false)
const fps = ref(0)
const detectionCount = ref(0)
const lastDetectionTime = ref(0)
const boxes = ref<DetectionBox[]>([])
const errorMsg = ref("")
const animationId = ref(0)

const CLASS_COLORS: Record<string, string> = {
  crazing: "border-red-500 bg-red-500/10 text-red-400",
  inclusion: "border-purple-500 bg-purple-500/10 text-purple-400",
  patches: "border-yellow-500 bg-yellow-500/10 text-yellow-400",
  pitted_surface: "border-blue-500 bg-blue-500/10 text-blue-400",
  "rolled-in_scale": "border-orange-500 bg-orange-500/10 text-orange-400",
  scratches: "border-green-500 bg-green-500/10 text-green-400",
}

const BOX_COLORS: Record<string, string> = {
  crazing: "#ef4444", inclusion: "#8b5cf6", patches: "#f59e0b",
  pitted_surface: "#3b82f6", "rolled-in_scale": "#f97316", scratches: "#22c55e",
}

function getTagClass(box: DetectionBox) {
  return CLASS_COLORS[box.class_name] || "border-gray-500 bg-gray-500/10 text-gray-400"
}

async function startCamera() {
  errorMsg.value = ""
  try {
    const s = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 640 }, height: { ideal: 480 }, frameRate: { ideal: 30 } },
      audio: false,
    })
    stream.value = s
    if (videoRef.value) {
      videoRef.value.srcObject = s
      await videoRef.value.play()
    }
    requestAnimationFrame(detectionLoop)
  } catch (e: any) {
    switch (e.name) {
      case "NotAllowedError": errorMsg.value = "摄像头权限被拒绝，请在浏览器设置中允许访问"; break
      case "NotFoundError": errorMsg.value = "未检测到摄像头设备"; break
      case "NotReadableError": errorMsg.value = "摄像头被其他应用占用"; break
      default: errorMsg.value = `无法访问摄像头: ${e.message || e.name}`
    }
  }
}

function togglePause() {
  isPaused.value = !isPaused.value
}

function stopCamera() {
  if (animationId.value) cancelAnimationFrame(animationId.value)
  if (stream.value) { stream.value.getTracks().forEach(t => t.stop()); stream.value = null }
  if (videoRef.value) videoRef.value.srcObject = null
  const canvas = canvasRef.value
  if (canvas) { const ctx = canvas.getContext("2d"); if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height) }
  boxes.value = []
  fps.value = 0
  detectionCount.value = 0
}

async function sendFrame(imageData: string) {
  const token = localStorage.getItem("token")
  try {
    const res = await fetch("/api/camera/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: JSON.stringify({ image: imageData }),
    })
    const json = await res.json()
    if (json.success && json.data) {
      boxes.value = json.data.boxes || []
      fps.value = json.data.fps || 0
      detectionCount.value = json.data.frame_index || 0
      lastDetectionTime.value = Math.round((json.data.detection_time || 0) * 1000)
    }
  } catch { /* skip single frame error */ }
}

function detectionLoop() {
  if (!stream.value) return
  animationId.value = requestAnimationFrame(detectionLoop)

  if (isPaused.value) { drawBoxes(); return }

  const video = videoRef.value
  const canvas = canvasRef.value
  if (!video || !canvas || video.readyState < 2) { drawBoxes(); return }

  canvas.width = video.videoWidth
  canvas.height = video.videoHeight

  const tempCanvas = document.createElement("canvas")
  tempCanvas.width = video.videoWidth
  tempCanvas.height = video.videoHeight
  const tempCtx = tempCanvas.getContext("2d")
  if (!tempCtx) return
  tempCtx.drawImage(video, 0, 0)

  const imageData = tempCanvas.toDataURL("image/jpeg", 0.7)
  sendFrame(imageData)
  drawBoxes()
}

function drawBoxes() {
  const canvas = canvasRef.value
  const video = videoRef.value
  if (!canvas || !video) return
  const ctx = canvas.getContext("2d")
  if (!ctx) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)
  const scaleX = canvas.width / (video.videoWidth || 640)
  const scaleY = canvas.height / (video.videoHeight || 480)

  for (const box of boxes.value) {
    const x1 = box.x1 * scaleX, y1 = box.y1 * scaleY
    const x2 = box.x2 * scaleX, y2 = box.y2 * scaleY
    const color = BOX_COLORS[box.class_name] || "#00ffff"

    ctx.strokeStyle = color
    ctx.lineWidth = 2
    ctx.strokeRect(x1, y1, x2 - x1, y2 - y1)

    ctx.fillStyle = color
    ctx.globalAlpha = 0.1
    ctx.fillRect(x1, y1, x2 - x1, y2 - y1)
    ctx.globalAlpha = 1

    const label = `${box.chinese_name || box.class_name} ${(box.confidence * 100).toFixed(0)}%`
    ctx.font = "12px sans-serif"
    const tw = ctx.measureText(label).width
    const lh = 16
    const ly = y1 >= lh ? y1 - lh : y1 + (y2 - y1)
    ctx.fillStyle = color
    ctx.fillRect(x1, ly, tw + 8, lh)
    ctx.fillStyle = "#ffffff"
    ctx.fillText(label, x1 + 4, ly + 12)
  }
}

onUnmounted(() => stopCamera())
</script>
