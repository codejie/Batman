import request from '@/utils/request'

export const getInfos = (data: any) =>
    request({
        url: '/strategy/finder/infos',
        method: 'post',
        data
    })

export const schedule = (data: any) =>
    request({
        url: '/strategy/finder/schedule',
        method: 'post',
        data        
    })

export const reschedule = (data: any) =>
    request({
        url: '/strategy/finder/reschedule',
        method: 'post',
        data
    })

export const getInstanceByStategy = (data: any) =>
    request({
        url: '/strategy/finder/instance',
        method: 'post',
        data
    })

export const getResultByInstance = (data: any) =>
    request({
        url: '/strategy/finder/result',
        method: 'post',
        data
    })
