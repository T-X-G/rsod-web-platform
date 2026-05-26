interface TargetResult {
  success: boolean; message?: string
  data?: {
    targets?: any[]; page?: number; limit?: number; total?: number
    id?: string; name?: string; type?: string; description?: string; image_url?: string
    created_at?: string; updated_at?: string
  }
}

export function getTargets(page?: number, limit?: number, type?: string | null): Promise<TargetResult>
export function getTarget(targetId: string): Promise<TargetResult>
export function createTarget(data: any): Promise<TargetResult>
export function updateTarget(targetId: string, data: any): Promise<TargetResult>
export function deleteTarget(targetId: string): Promise<{ success: boolean; message?: string }>
