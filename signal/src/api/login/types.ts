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

export type UserRequest = {
  account: string
  passwd: string
}

export type UserResponse = {
  accessToken: string
  refreshToken?: string
  expired?: Date
}

export type UserInfo = {
  account: string
  passwd: string
  accessToken?: string
  refreshToken?: string
  expired?: Date
}