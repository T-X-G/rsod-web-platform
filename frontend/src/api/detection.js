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
