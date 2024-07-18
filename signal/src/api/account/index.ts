import request from '@/axios'
// import type { UserType } from './types'
import type { LoginRequest, LoginResponse, LogoutRequest, LogoutResponse } from './types'

// interface RoleParams {
//   roleName: string
// }

// export const loginApi = (data: UserType): Promise<IResponse<UserType>> => {
//   return request.post({ url: '/mock/user/login', data })
// }

export const apiLogout = (data?: LogoutRequest): Promise<Response<LogoutResponse>> => {
  return request.post({ 
    url: '/account/logout',
    data
   })
}

// export const getAdminRoleApi = (
//   params: RoleParams
// ): Promise<IResponse<AppCustomRouteRecordRaw[]>> => {
//   return request.get({ url: '/mock/role/list', params })
// }

// export const getTestRoleApi = (params: RoleParams): Promise<IResponse<string[]>> => {
//   return request.get({ url: '/mock/role/list2', params })
// }

export const apiLogin = (data: LoginRequest): Promise<Response<LoginResponse>> => {
  return request.post({
    url: '/account/login',
    data
  })
}
