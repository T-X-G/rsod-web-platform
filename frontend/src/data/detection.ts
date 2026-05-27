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
