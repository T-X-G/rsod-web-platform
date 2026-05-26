interface DetectionRecord {
  id: string; filename: string; total_objects: number; detection_time: number
  result_image_url: string; created_at: string; status: string
}
interface DetectionResult {
  success: boolean; message?: string
  data?: {
    id?: string; total_objects?: number; detection_time?: number
    boxes?: any[]; result_image_url?: string; model_name?: string
    records?: DetectionRecord[]; total?: number; page?: number; limit?: number
  }
}

export function detectSingle(file: File, modelName?: string): Promise<DetectionResult>
export function detectBatch(files: File[], modelName?: string): Promise<DetectionResult>
export function getHistory(page?: number, limit?: number): Promise<DetectionResult>
export function getDetail(recordId: string): Promise<DetectionResult>
export function deleteRecord(recordId: string): Promise<{ success: boolean; message?: string }>
