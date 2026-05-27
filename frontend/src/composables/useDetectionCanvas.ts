import { ref, type Ref } from "vue"

export interface DetectionBox {
  x1: number; y1: number; x2: number; y2: number
  confidence: number; class_name: string; chinese_name: string
}

const BOX_COLORS: Record<string, string> = {
  crazing: "#ef4444", inclusion: "#8b5cf6", patches: "#f59e0b",
  pitted_surface: "#3b82f6", "rolled-in_scale": "#f97316", scratches: "#22c55e",
}

export function useDetectionCanvas(canvasRef: Ref<HTMLCanvasElement | null>) {
  let lastBoxes: DetectionBox[] = []
  let lastWidth = 0
  let lastHeight = 0

  function drawBoxes(
    boxes: DetectionBox[],
    videoWidth: number,
    videoHeight: number,
    displayWidth: number,
    displayHeight: number,
    interpolate = false,
  ) {
    const canvas = canvasRef.value
    if (!canvas) return
    canvas.width = displayWidth
    canvas.height = displayHeight
    const ctx = canvas.getContext("2d")!
    ctx.clearRect(0, 0, displayWidth, displayHeight)

    const source = interpolate && lastBoxes.length ? lastBoxes : boxes
    const srcW = interpolate ? lastWidth : videoWidth
    const srcH = interpolate ? lastHeight : videoHeight
    const scaleX = displayWidth / (srcW || 1)
    const scaleY = displayHeight / (srcH || 1)

    for (const box of source) {
      const x1 = box.x1 * scaleX
      const y1 = box.y1 * scaleY
      const x2 = box.x2 * scaleX
      const y2 = box.y2 * scaleY
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
      const ly = y1 >= 16 ? y1 - 16 : y1 + (y2 - y1)
      ctx.fillStyle = color
      ctx.fillRect(x1, ly, tw + 8, 16)
      ctx.fillStyle = "#ffffff"
      ctx.fillText(label, x1 + 4, ly + 12)
    }

    if (!interpolate) {
      lastBoxes = boxes
      lastWidth = videoWidth
      lastHeight = videoHeight
    }
  }

  function clearCanvas() {
    const canvas = canvasRef.value
    if (canvas) canvas.getContext("2d")!.clearRect(0, 0, canvas.width, canvas.height)
  }

  function resetInterpolation() {
    lastBoxes = []
    lastWidth = 0
    lastHeight = 0
  }

  return { drawBoxes, clearCanvas, resetInterpolation }
}
