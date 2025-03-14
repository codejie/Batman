import request from '@/axios'
import type { UserLoginType, UserType } from './types'

// interface RoleParams {
//   roleName: string
// }

export const loginApi = (data: UserLoginType): Promise<IResponse<UserType>> => {
  return request.post({ url: '/account/login', data })
}

export const loginOutApi = (): Promise<IResponse> => {
  return request.post({ url: '/account/logout', data: {} })
}

// export const getUserListApi = ({ params }: AxiosConfig) => {
//   return request.get<{
//     code: string
//     data: {
//       list: UserType[]
//       total: number
//     }
//   }>({ url: '/mock/user/list', params })
// }

// export const getAdminRoleApi = (
//   params: RoleParams
// ): Promise<IResponse<AppCustomRouteRecordRaw[]>> => {
//   return request.get({ url: '/mock/role/list', params })
// }

// export const getTestRoleApi = (params: RoleParams): Promise<IResponse<string[]>> => {
//   return request.get({ url: '/mock/role/list2', params })
// }
