export interface UserLoginType {
  account: string
  passwd: string
}

export interface UserType {
  account: string
  passwd: string
  accessToken?: string
  refreshToken?: string
  expired?: Date
  avatar?: string
}
