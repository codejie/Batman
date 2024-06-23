import request from '@/axios'
// import type { UserType } from './types'
import type { UserRequest, UserResponse } from './types'

// interface RoleParams {
//   roleName: string
// }

// export const loginApi = (data: UserType): Promise<IResponse<UserType>> => {
//   return request.post({ url: '/mock/user/login', data })
// }

export const loginOutApi = (): Promise<Response> => {
  return request.get({ url: '/mock/user/loginOut' })
}

// export const getAdminRoleApi = (
//   params: RoleParams
// ): Promise<IResponse<AppCustomRouteRecordRaw[]>> => {
//   return request.get({ url: '/mock/role/list', params })
// }

// export const getTestRoleApi = (params: RoleParams): Promise<IResponse<string[]>> => {
//   return request.get({ url: '/mock/role/list2', params })
// }

export const apiLogin = (data: UserRequest): Promise<Response<UserResponse>> => {
  return request.post({
    url: '/account/login',
    data
  })
}
