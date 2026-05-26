export type DetectionSeverity = "low" | "medium" | "high";

export interface DetectionBox {
  label: string;
  confidence: number;
  bbox: [number, number, number, number];
  severity: DetectionSeverity;
  color: string;
}

export interface DetectionItem {
  id: string;
  fileName: string;
  fileSize: number;
  originalImage: string;
  resultImage: string;
  detections: DetectionBox[];
  status: "pending" | "running" | "completed" | "paused" | "failed";
  progress: number;
  createdAt: number;
  updatedAt: number;
}

const detectionLabels = [
  { label: "裂纹", severity: "high" as DetectionSeverity, color: "#ef4444" },
  { label: "斑点", severity: "medium" as DetectionSeverity, color: "#f59e0b" },
  { label: "划痕", severity: "low" as DetectionSeverity, color: "#22c55e" },
  { label: "麻面", severity: "medium" as DetectionSeverity, color: "#3b82f6" },
  { label: "夹杂物", severity: "high" as DetectionSeverity, color: "#8b5cf6" },
];

function hashSeed(input: string) {
  let hash = 0;
  for (let i = 0; i < input.length; i += 1) {
    hash = Math.imul(31, hash) + input.charCodeAt(i);
  }
  return Math.abs(hash);
}

function sampleFromSeed(seed: number, max: number) {
  const value = Math.sin(seed) * 10000;
  return Math.floor(Math.abs(value) % max);
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}

export function generateMockDetections(fileName: string): DetectionBox[] {
  const seed = hashSeed(fileName + Date.now());
  const count = 2 + (seed % 4);
  const boxes: DetectionBox[] = [];

  for (let idx = 0; idx < count; idx += 1) {
    const labelSeed = seed + idx * 31;
    const labelData = detectionLabels[labelSeed % detectionLabels.length];
    const x = clamp((sampleFromSeed(labelSeed + 11, 70) + idx * 3) % 82, 4, 78);
    const y = clamp((sampleFromSeed(labelSeed + 23, 65) + idx * 5) % 78, 6, 74);
    const width = clamp(12 + (sampleFromSeed(labelSeed + 37, 30) % 38), 10, 44);
    const height = clamp(
      14 + (sampleFromSeed(labelSeed + 53, 28) % 38),
      10,
      44,
    );
    const confidence = clamp(
      0.65 + sampleFromSeed(labelSeed + 71, 30) / 100,
      0.65,
      0.98,
    );

    boxes.push({
      label: labelData.label,
      confidence: Number(confidence.toFixed(2)),
      bbox: [x, y, width, height],
      severity: labelData.severity,
      color: labelData.color,
    });
  }

  return boxes;
}

export function createDetectionItem(file: File): Promise<DetectionItem> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result as string;
      resolve({
        id: `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`,
        fileName: file.name,
        fileSize: file.size,
        originalImage: dataUrl,
        resultImage: dataUrl,
        detections: [],
        status: "pending",
        progress: 0,
        createdAt: Date.now(),
        updatedAt: Date.now(),
      });
    };
    reader.onerror = () => reject(new Error("读取文件失败"));
    reader.readAsDataURL(file);
  });
}

export function buildMockDetectionResult(item: DetectionItem): DetectionItem {
  return {
    ...item,
    resultImage: item.originalImage,
    detections: generateMockDetections(item.fileName),
    updatedAt: Date.now(),
  };
}
