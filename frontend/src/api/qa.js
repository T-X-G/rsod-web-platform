// @ts-nocheck
import request from './request'

export const chat = (messages, conversationId = null) => {
  return request.post('/api/qa/chat', {
    messages,
    conversation_id: conversationId,
    user_id: localStorage.getItem('user_id') || 'default_user',
  })
}

export const chatStream = async (messages, conversationId = null, onToken, onDone) => {
  const token = localStorage.getItem('token')
  const res = await fetch('/api/qa/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({
      messages,
      conversation_id: conversationId,
      user_id: localStorage.getItem('user_id') || 'default_user',
    }),
  })

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buf = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buf += decoder.decode(value, { stream: true })
    const lines = buf.split('\n')
    buf = lines.pop() || ''
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6))
        if (data.error) { onDone(data); return }
        if (data.token) onToken(data)
        if (data.done) { onDone(data); return }
      }
    }
  }
}

export const getConversations = (limit = 10, offset = 0) => {
  return request.get('/api/qa/conversations', { params: { limit, offset } })
}

export const getConversation = (conversationId) => {
  return request.get(`/api/qa/conversation/${conversationId}`)
}

export const updateConversation = (conversationId, title) => {
  return request.put(`/api/qa/conversation/${conversationId}`, { title })
}

export const deleteConversation = (conversationId) => {
  return request.delete(`/api/qa/conversation/${conversationId}`)
}
