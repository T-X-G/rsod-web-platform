// @ts-nocheck
import request from './request'

export const detectSingle = (file, modelName = 'steel-defect-yolo11n') => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('model_name', modelName)
  return request.post('/api/detection/single', formData)
}

export const detectBatch = (files, modelName = 'steel-defect-yolo11n') => {
  const formData = new FormData()
  for (const file of files) {
    formData.append('files', file)
  }
  formData.append('model_name', modelName)
  return request.post('/api/detection/batch', formData)
}

export const getHistory = (page = 1, limit = 10) => {
  return request.get('/api/detection/history', { params: { page, limit } })
}

export const getDetail = (recordId) => {
  return request.get(`/api/detection/detail/${recordId}`)
}

export const deleteRecord = (recordId) => {
  return request.delete(`/api/detection/${recordId}`)
}

export const getVideoInfo = (file) => {
  const fd = new FormData(); fd.append('file', file)
  return request.post('/api/video-detection/info', fd)
}

export const detectRealtimeFrame = (formData) => {
  return request.post('/api/video-detection/realtime-frame', formData)
}

export const detectFullVideo = (file, frameInterval, conf, iou) => {
  const fd = new FormData()
  fd.append('file', file)
  fd.append('frame_interval', frameInterval)
  fd.append('confidence_threshold', conf)
  fd.append('iou_threshold', iou)
  return request.post('/api/video-detection/full', fd)
}

export const getVideoProgress = (taskId) => {
  return request.get(`/api/video-detection/progress/${taskId}`)
}

export const cancelVideoDetection = (taskId) => {
  return request.post(`/api/video-detection/cancel/${taskId}`)
}
