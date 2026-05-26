interface QAResult {
  success: boolean; message?: string
  data?: {
    conversation_id?: number; response?: string; messages?: any[]
    conversations?: { id: number; title: string; created_at?: string; updated_at?: string }[]
    title?: string
  }
}

export function chat(messages: object[], conversationId?: number | null): Promise<QAResult>
export function chatStream(
  messages: object[], conversationId: number | null | undefined,
  onToken: (data: any) => void, onDone: (data: any) => void
): Promise<void>
export function getConversations(limit?: number, offset?: number): Promise<QAResult>
export function getConversation(conversationId: number): Promise<QAResult>
export function updateConversation(conversationId: number, title: string): Promise<QAResult>
export function deleteConversation(conversationId: number): Promise<QAResult>
