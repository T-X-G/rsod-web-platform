// @ts-nocheck
import request from './request'

export const login = (username, password) => {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  return request.post('/api/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
}

export const register = (username, password, email) => {
  return request.post('/api/auth/register', { username, password, email })
}

export const logout = () => {
  return request.post('/api/auth/logout')
}

export const getMe = () => {
  return request.get('/api/auth/me')
}
