// @ts-nocheck
import request from './request'

export const login = (username, password) => {
  const params = new URLSearchParams()
  params.append('username', username)
  params.append('password', password)
  return request.post('/api/auth/login', params, {
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
