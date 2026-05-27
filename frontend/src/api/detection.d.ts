export interface DetectionRecord {
  id: string; filename: string; total_objects: number; detection_time: number
  result_image_url: string; created_at: string; status: string
}
export interface DetectionResult {
  success: boolean; message?: string
  data?: {
    id?: string; total_objects?: number; detection_time?: number
    boxes?: any[]; result_image_url?: string; model_name?: string
    records?: DetectionRecord[]; total?: number; page?: number; limit?: number
  }
}
export interface VideoInfoResult {
  success: boolean; message?: string
  data?: { fps: number; frame_count: number; duration: number; width: number; height: number }
}
export interface FrameDetectResult {
  success: boolean; message?: string
  data?: { boxes: any[]; total_objects: number; detection_time: number; image_width: number; image_height: number }
}
export interface FullVideoResult {
  success: boolean; message?: string
  data?: { task_id: string }
}
export interface TaskProgressResult {
  success: boolean; message?: string
  data?: { status: string; progress: number; frames_processed: number; total_frames: number }
}

export function detectSingle(file: File, modelName?: string): Promise<DetectionResult>
export function detectBatch(files: File[], modelName?: string): Promise<DetectionResult>
export function getHistory(page?: number, limit?: number): Promise<DetectionResult>
export function getDetail(recordId: string): Promise<DetectionResult>
export function deleteRecord(recordId: string): Promise<{ success: boolean; message?: string }>
export function getVideoInfo(file: File): Promise<VideoInfoResult>
export function detectRealtimeFrame(formData: FormData): Promise<FrameDetectResult>
export function detectFullVideo(file: File, frameInterval: number, conf: number, iou: number): Promise<FullVideoResult>
export function getVideoProgress(taskId: string): Promise<TaskProgressResult>
export function cancelVideoDetection(taskId: string): Promise<{ success: boolean; message?: string }>
