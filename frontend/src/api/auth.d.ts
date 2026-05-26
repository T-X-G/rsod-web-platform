interface TokenData { access_token: string; token_type: string; user_id: string; username: string }
interface AuthResult {
  success: boolean
  message?: string
  data?: TokenData & {
    id?: string; username?: string; email?: string; role?: string; created_at?: string
  }
}

export function login(username: string, password: string): Promise<AuthResult>
export function register(username: string, password: string, email?: string): Promise<AuthResult>
export function logout(): Promise<{ success: boolean; message?: string }>
export function getMe(): Promise<AuthResult>
