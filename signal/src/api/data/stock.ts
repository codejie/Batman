import request from '@/utils/request'

export const getStockHistory = (data: any) =>
    request({
        url: '/data/stock/history',
        method: 'post',
        data
    })