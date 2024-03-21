import request from '@/utils/request'

export const getInfo = (data: any) =>
    request({
        url: '/strategy/finder/info',
        method: 'post',
        data
    })

export const schedule = (data: any) =>
    request({
        url: '/strategy/finder/schedule',
        method: 'post',
        data        
    })