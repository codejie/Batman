import request from '@/utils/request'

export const getPersonalized = (data: any) =>
    request({
        url: '/quotes/personalized/infos',
        method: 'post',
        data
    })