import request from '@/utils/request'

export const getPersonalized = (data: any) =>
    request({
        url: '/quotes/personalized/infos',
        method: 'post',
        data
    })

export const creatPersonalized = (data: any) =>
    request({
        url: '/quotes/personalized/create',
        method: 'post',
        data
    })

export const removePersonalized = (data: any) =>
    request({
        url: '/quotes/personalized/remove',
        method: 'post',
        data
    })