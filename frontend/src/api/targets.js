import request from './request'

export const getTargets = (page = 1, limit = 10, type = null) => {
  return request.get('/api/targets/list', { params: { page, limit, type } })
}

export const getTarget = (targetId) => {
  return request.get(`/api/targets/${targetId}`)
}

export const createTarget = (data) => {
  const formData = new FormData()
  formData.append('name', data.name)
  if (data.type) formData.append('type', data.type)
  if (data.description) formData.append('description', data.description)
  if (data.image) formData.append('image', data.image)
  return request.post('/api/targets/', formData)
}

export const updateTarget = (targetId, data) => {
  const formData = new FormData()
  if (data.name) formData.append('name', data.name)
  if (data.type) formData.append('type', data.type)
  if (data.description) formData.append('description', data.description)
  if (data.image) formData.append('image', data.image)
  return request.put(`/api/targets/${targetId}`, formData)
}

export const deleteTarget = (targetId) => {
  return request.delete(`/api/targets/${targetId}`)
}
