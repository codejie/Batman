export type UserLoginType = {
  username: string
  password: string
}

export type UserType = {
  username: string
  password: string
  role: string
  roleId: string
  permissions: string | string[]
}

export type LoginRequest = {
  account: string
  passwd: string
}

export type LoginResponse = {
  accessToken: string
  refreshToken?: string
  expired?: Date
  // uid: number
  avatar?: string
}

export type LogoutRequest = {}
export type LogoutResponse = {}

export type UserInfo = {
  // account: string
  // passwd: string
  accessToken?: string
  refreshToken?: string
  expired?: Date
  // uid?: number
  avatar?: string
}