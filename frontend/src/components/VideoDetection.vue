<template>
  <DashboardLayout>
    <div class="space-y-6">
      <div>
        <h1 class="text-2xl font-bold text-white mb-2">视频检测</h1>
        <p class="text-gray-400">上传视频文件或输入视频 URL，实时检测或完整处理</p>
      </div>

      <div class="flex gap-4 flex-col xl:flex-row">
        <!-- Left: Video Player -->
        <div class="flex-1 glass-card p-6 space-y-4">
          <!-- Input Source Tabs -->
          <div class="flex gap-1 mb-2">
            <button @click="sourceType = 'file'" :class="sourceType === 'file' ? 'bg-primary/20 text-primary' : 'text-gray-400 hover:text-white'"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all">
              📁 文件上传
            </button>
            <button @click="sourceType = 'url'" :class="sourceType === 'url' ? 'bg-primary/20 text-primary' : 'text-gray-400 hover:text-white'"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all">
              🔗 URL 输入
            </button>
          </div>

          <!-- File Upload -->
          <div v-if="sourceType === 'file'" @dragover="handleDragOver" @drop="handleDrop"
            @click="triggerFileInput"
            class="border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all"
            :class="videoSrc ? 'border-primary/30 bg-primary/5' : 'border-white/10 hover:border-primary/50 hover:bg-white/5'">
            <input type="file" accept="video/*" ref="fileInput" class="hidden" @change="handleFileSelect" />
            <div v-if="!videoSrc">
              <svg class="w-12 h-12 mx-auto mb-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="text-sm text-gray-400">点击或拖拽视频文件到此处</p>
              <p class="text-xs text-gray-500 mt-1">mp4 / avi / mov / webm / mkv (≤200MB)</p>
            </div>
            <div v-else>
              <img v-if="thumbnail" :src="thumbnail" class="max-h-32 mx-auto rounded-lg mb-2" />
              <p class="text-sm text-primary">已加载</p>
            </div>
          </div>

          <!-- URL Input -->
          <div v-if="sourceType === 'url'" class="flex gap-2">
            <input v-model="videoUrl" type="text" placeholder="https://example.com/video.mp4"
              class="flex-1 px-4 py-3 bg-white/5 border border-primary/20 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary/50" />
            <button @click="loadUrlVideo" class="px-6 py-3 bg-gradient-to-r from-primary to-cyan-400 text-white rounded-xl font-medium text-sm">
              加载
            </button>
          </div>

          <!-- Error Msg -->
          <div v-if="errorMsg" class="px-4 py-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm">
            {{ errorMsg }}
          </div>

          <!-- Video Player -->
          <div ref="videoContainer" class="relative bg-black rounded-2xl overflow-hidden" style="min-height: 300px;">
            <video v-if="videoSrc" ref="videoRef" :src="videoSrc" class="w-full object-contain" style="max-height: 480px;"
              @loadeddata="onLoaded" @play="onPlay" @pause="onPause" @seeked="onSeeked" @ended="onEnded"
              @error="onVideoError" controls />
            <canvas ref="canvasRef" class="absolute inset-0 w-full h-full pointer-events-none" />
            <div v-if="!videoSrc" class="absolute inset-0 flex items-center justify-center text-gray-500">
              <p class="text-sm">{{ sourceType === 'file' ? '请上传视频' : '请输入视频 URL' }}</p>
            </div>
          </div>

          <!-- Info -->
          <div v-if="videoInfo" class="flex gap-4 text-xs text-gray-400">
            <span>{{ videoInfo.width }}×{{ videoInfo.height }}</span>
            <span>{{ formatTime(videoInfo.duration) }}</span>
            <span v-if="videoInfo.fps > 0">{{ videoInfo.fps.toFixed(0) }}fps</span>
          </div>
        </div>

        <!-- Right: Controls -->
        <div class="w-80 flex-shrink-0 glass-card p-6 space-y-5">
          <!-- Mode -->
          <div>
            <label class="text-sm text-gray-300 font-medium mb-2 block">检测模式</label>
            <div class="flex gap-1">
              <button @click="detectionMode = 'realtime'" :class="detectionMode === 'realtime' ? 'bg-primary/20 text-primary' : 'text-gray-400'"
                class="flex-1 px-3 py-2 rounded-lg text-sm transition-all">实时</button>
              <button @click="detectionMode = 'full'" :class="detectionMode === 'full' ? 'bg-primary/20 text-primary' : 'text-gray-400'"
                class="flex-1 px-3 py-2 rounded-lg text-sm transition-all">完整</button>
            </div>
          </div>

          <!-- FPS Slider (realtime) -->
          <div v-if="detectionMode === 'realtime'">
            <label class="text-sm text-gray-300 font-medium mb-2 flex justify-between">
              <span>检测频率</span>
              <span class="text-primary">{{ detectionFPS }} fps</span>
            </label>
            <input type="range" v-model.number="detectionFPS" min="2" max="15" step="1" :disabled="isRunning"
              class="w-full accent-primary" />
          </div>

          <!-- Frame Interval (full) -->
          <div v-if="detectionMode === 'full'">
            <label class="text-sm text-gray-300 font-medium mb-2 flex justify-between">
              <span>帧间隔</span>
              <span class="text-primary">每 {{ frameInterval }} 帧</span>
            </label>
            <input type="range" v-model.number="frameInterval" min="1" max="10" step="1" :disabled="isRunning"
              class="w-full accent-primary" />
          </div>

          <!-- Confidence -->
          <div>
            <label class="text-sm text-gray-300 font-medium mb-2 flex justify-between">
              <span>置信度</span>
              <span class="text-primary">{{ confidenceThreshold.toFixed(2) }}</span>
            </label>
            <input type="range" v-model.number="confidenceThreshold" min="0.01" max="0.9" step="0.01" :disabled="isRunning"
              class="w-full accent-primary" />
          </div>

          <!-- Buttons -->
          <div class="flex gap-2">
            <button v-if="!isRunning" @click="startDetection" :disabled="!videoSrc"
              class="flex-1 px-4 py-3 bg-gradient-to-r from-primary to-cyan-400 text-white rounded-xl font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed">
              开始检测
            </button>
            <button v-else @click="stopDetection"
              class="flex-1 px-4 py-3 border border-red-500/20 text-red-400 rounded-xl font-medium text-sm hover:bg-red-500/10">
              停止检测
            </button>
          </div>

          <!-- Progress (full mode) -->
          <div v-if="detectionMode === 'full' && isRunning && fullProgress > 0" class="space-y-1">
            <div class="h-2 bg-white/10 rounded-full overflow-hidden">
              <div class="h-full bg-gradient-to-r from-primary to-cyan-400 rounded-full transition-all"
                :style="{ width: (fullProgress * 100).toFixed(0) + '%' }" />
            </div>
            <p class="text-xs text-gray-400 text-center">
              {{ (fullProgress * 100).toFixed(0) }}%
              <span v-if="fullProgress > 0 && fullProgress < 1">
                · 预计剩余 {{ formatEstimate(fullElapsed / fullProgress * (1 - fullProgress)) }}
              </span>
            </p>
            <button @click="cancelFullDetection" class="w-full text-xs text-gray-400 hover:text-red-400">取消</button>
          </div>

          <!-- Full Result Panel -->
          <div v-if="detectionMode === 'full' && fullResult" class="space-y-3">
            <div class="grid grid-cols-2 gap-2 text-center">
              <div class="bg-white/5 rounded-lg p-2">
                <span class="text-primary text-lg font-bold block">{{ fullResult.total_frames }}</span>
                <span class="text-gray-500 text-xs">总帧数</span>
              </div>
              <div class="bg-white/5 rounded-lg p-2">
                <span class="text-green-400 text-lg font-bold block">{{ fullResult.detected_frames }}</span>
                <span class="text-gray-500 text-xs">检测帧数</span>
              </div>
            </div>
            <div v-if="fullResult.frames_data?.[0]?.total_objects !== undefined" class="text-center">
              <span class="text-gray-400 text-xs">累计检测目标</span>
              <span class="text-primary text-xl font-bold block">{{ fullResult.frames_data.reduce((s: number, f: any) => s + (f.total_objects || 0), 0) }}</span>
            </div>
          </div>

          <!-- Stats -->
          <div v-if="stats.totalFrames > 0" class="grid grid-cols-2 gap-2 text-center">
            <div class="bg-white/5 rounded-lg p-2">
              <span class="text-primary text-lg font-bold block">{{ stats.totalFrames }}</span>
              <span class="text-gray-500 text-xs">检测帧数</span>
            </div>
            <div class="bg-white/5 rounded-lg p-2">
              <span class="text-green-400 text-lg font-bold block">{{ currentBoxes.length }}</span>
              <span class="text-gray-500 text-xs">当前目标</span>
            </div>
          </div>

          <!-- Detected objects -->
          <div v-if="currentBoxes.length > 0" class="space-y-1">
            <h4 class="text-sm font-medium text-gray-300">检测目标</h4>
            <div class="flex gap-1 flex-wrap">
              <span v-for="(box, i) in currentBoxes" :key="i"
                class="px-2 py-1 rounded-full text-xs font-medium border"
                :class="getTagClass(box.class_name)">
                {{ box.chinese_name || box.class_name }} {{ (box.confidence * 100).toFixed(0) }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from "vue"
import DashboardLayout from "../layouts/DashboardLayout.vue"
import { useDetectionCanvas } from "../composables/useDetectionCanvas"
import { useVideoInput } from "../composables/useVideoInput"
import { getVideoInfo, detectRealtimeFrame, detectFullVideo, getVideoProgress, cancelVideoDetection } from "../api/detection"

type DetectionBox = { x1: number; y1: number; x2: number; y2: number; confidence: number; class_name: string; chinese_name: string }

const fileInput = ref<HTMLInputElement | null>(null)
const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const videoContainer = ref<HTMLDivElement | null>(null)

const { drawBoxes, clearCanvas, resetInterpolation } = useDetectionCanvas(canvasRef)

const videoSrc = ref("")
const { sourceType, videoUrl, thumbnail, errorMsg, handleFileSelect, handleDrop, handleDragOver, loadUrlVideo, reset: resetInput } = useVideoInput(videoSrc)

const detectionMode = ref<"realtime" | "full">("realtime")
const detectionFPS = ref(5)
const frameInterval = ref(3)
const confidenceThreshold = ref(0.25)
const isRunning = ref(false)
const currentBoxes = ref<DetectionBox[]>([])
const videoInfo = ref<{ fps: number; frame_count: number; duration: number; width: number; height: number } | null>(null)
const fullProgress = ref(0)
const fullTaskId = ref("")
const fullResult = ref<{ total_frames: number; detected_frames: number; frames_data: any[] } | null>(null)
const fullElapsed = ref(0)
const stats = ref({ totalFrames: 0 })

let captureTimer: ReturnType<typeof setInterval> | null = null
let animFrameId = 0
let fullPollTimer: ReturnType<typeof setInterval> | null = null
let resizeObserver: ResizeObserver | null = null
let fullStartTime = 0
let videoWidth = 0, videoHeight = 0

const TAG_COLORS: Record<string, string> = {
  crazing: "border-red-500 bg-red-500/10 text-red-400",
  inclusion: "border-purple-500 bg-purple-500/10 text-purple-400",
  patches: "border-yellow-500 bg-yellow-500/10 text-yellow-400",
  pitted_surface: "border-blue-500 bg-blue-500/10 text-blue-400",
  "rolled-in_scale": "border-orange-500 bg-orange-500/10 text-orange-400",
  scratches: "border-green-500 bg-green-500/10 text-green-400",
}
function getTagClass(cn: string) { return TAG_COLORS[cn] || "border-gray-500 bg-gray-500/10 text-gray-400" }
function formatTime(s: number) {
  if (!s || s <= 0) return "--:--"
  const m = Math.floor(s / 60), sec = Math.floor(s % 60)
  return `${m.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`
}
function formatEstimate(s: number) {
  if (s < 1) return "不到1秒"
  if (s < 60) return `${Math.ceil(s)}秒`
  return `${Math.ceil(s / 60)}分钟`
}

function triggerFileInput() { fileInput.value?.click() }

// Video lifecycle
async function onLoaded() {
  const v = videoRef.value; if (!v) return
  videoWidth = v.videoWidth; videoHeight = v.videoHeight
  try {
    const blob = await fetch(videoSrc.value).then(r => r.blob())
    const fd = new FormData(); fd.append("file", blob, "video.mp4")
    const res = await getVideoInfo(blob as any)
    if (res.success) videoInfo.value = res.data || null
  } catch { /* ignore */ }
}
function onPlay() { if (isRunning.value && detectionMode.value === "realtime") startCapture() }
function onPause() { stopCapture() }
function onSeeked() { clearCanvas(); resetInterpolation() }
function onEnded() { if (detectionMode.value === "realtime") stopDetection() }
function onVideoError() {
  const v = videoRef.value
  if (v?.error) {
    switch (v.error.code) {
      case MediaError.MEDIA_ERR_SRC_NOT_SUPPORTED: errorMsg.value = "视频格式不支持，请使用 mp4/webm 格式"; break
      case MediaError.MEDIA_ERR_NETWORK: errorMsg.value = "网络错误，无法加载视频"; break
      case MediaError.MEDIA_ERR_DECODE: errorMsg.value = "视频解码失败，编码不兼容"; break
      default: errorMsg.value = "视频加载失败"
    }
  } else {
    errorMsg.value = "视频加载失败，请检查格式或网络"
  }
}

// Realtime capture
function startCapture() {
  stopCapture()
  const interval = Math.floor(1000 / detectionFPS.value)
  captureTimer = setInterval(captureFrame, interval)
  animFrameId = requestAnimationFrame(animationLoop)
}
function stopCapture() {
  if (captureTimer) { clearInterval(captureTimer); captureTimer = null }
  if (animFrameId) { cancelAnimationFrame(animFrameId); animFrameId = 0 }
}

async function captureFrame() {
  const v = videoRef.value; if (!v || v.paused || v.ended) return
  const temp = document.createElement("canvas")
  temp.width = v.videoWidth; temp.height = v.videoHeight
  temp.getContext("2d")!.drawImage(v, 0, 0)
  const blob = await new Promise<Blob | null>(r => temp.toBlob(b => r(b), "image/jpeg", 0.6))
  if (!blob) return
  const fd = new FormData(); fd.append("file", blob, "frame.jpg")
  fd.append("confidence_threshold", confidenceThreshold.value.toString())
  try {
    const res = await detectRealtimeFrame(fd)
    if (res.success && res.data) {
      currentBoxes.value = res.data.boxes || []
      stats.value.totalFrames++
    }
  } catch { /* skip single frame */ }
}

function animationLoop() {
  if (!isRunning.value) return
  animFrameId = requestAnimationFrame(animationLoop)
  const v = videoRef.value; const c = canvasRef.value
  if (!v || !c) return
  drawBoxes(currentBoxes.value, videoWidth || v.videoWidth, videoHeight || v.videoHeight, c.width || v.clientWidth, c.height || v.clientHeight)
}

// Full detection
async function startFullDetection() {
  if (!videoSrc.value) return
  isRunning.value = true
  fullResult.value = null
  fullStartTime = Date.now()
  fullElapsed.value = 0
  try {
    const blob = await fetch(videoSrc.value).then(r => r.blob())
    const res = await detectFullVideo(new File([blob], "video.mp4", { type: "video/mp4" }), frameInterval.value, confidenceThreshold.value, 0.7)
    if (res.success && res.data) {
      fullTaskId.value = res.data.task_id
      fullPollTimer = setInterval(pollProgress, 3000)
    } else {
      isRunning.value = false
      errorMsg.value = res.message || "启动处理失败"
    }
  } catch { isRunning.value = false; errorMsg.value = "网络错误" }
}
async function pollProgress() {
  try {
    const res = await getVideoProgress(fullTaskId.value)
    if (!res.success) { stopDetection(); return }
    fullProgress.value = res.data!.progress || 0
    fullElapsed.value = (Date.now() - fullStartTime) / 1000
    if (res.data!.status !== "processing") {
      stopFullDetection()
      if (res.data!.status === "completed") {
        await fetchFullResult()
      } else if (res.data!.status === "failed") {
        errorMsg.value = "检测处理失败"
      }
    }
  } catch { /* retry next poll */ }
}
async function fetchFullResult() {
  try {
    const res = await (await fetch(`/api/video-detection/result/${fullTaskId.value}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })).json()
    if (res.success && res.data?.result) {
      fullResult.value = res.data.result
    }
  } catch { /* ignore */ }
}
async function cancelFullDetection() {
  await cancelVideoDetection(fullTaskId.value)
  stopFullDetection()
}
function stopFullDetection() {
  if (fullPollTimer) { clearInterval(fullPollTimer); fullPollTimer = null }
  isRunning.value = false
}

// Start/Stop
function startDetection() {
  errorMsg.value = ""
  if (detectionMode.value === "full") { startFullDetection(); return }
  isRunning.value = true
  fullProgress.value = 0
  const v = videoRef.value
  if (v) {
    nextTick(() => { if (canvasRef.value && v) {
      canvasRef.value.width = v.clientWidth; canvasRef.value.height = v.clientHeight
    }})
    v.play().then(() => startCapture()).catch(() => { startCapture() })
  }
}
function stopDetection() {
  stopCapture()
  stopFullDetection()
  isRunning.value = false
  clearCanvas()
  currentBoxes.value = []
  stats.value.totalFrames = 0
}

// Visibility
function handleVisibility() {
  if (document.hidden) { stopCapture() }
  else if (isRunning.value) { startCapture() }
}

// ResizeObserver
onMounted(() => {
  document.addEventListener("visibilitychange", handleVisibility)
  if (videoContainer.value) {
    resizeObserver = new ResizeObserver(() => {
      const v = videoRef.value; const c = canvasRef.value
      if (v && c) { c.width = v.clientWidth; c.height = v.clientHeight }
    })
    resizeObserver.observe(videoContainer.value)
  }
})

onUnmounted(() => {
  stopDetection()
  document.removeEventListener("visibilitychange", handleVisibility)
  if (resizeObserver) resizeObserver.disconnect()
  resetInput()
})

watch(videoSrc, () => {
  stopDetection()
  videoInfo.value = null
})
</script>
