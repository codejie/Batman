import request from '@/axios'
import * as Types from './types'

export const apiNewHigh = (data: Types.NewHighRequest): Promise<IResponse<Types.NewHighResult>> => {
  return request.post({
    url: '/data/third/stock/new_high',
    data
  })
}

export const apiUptrend = (data: Types.UptrendRequest): Promise<IResponse<Types.UptrendResult>> => {
  return request.post({
    url: '/data/third/stock/uptrend',
    data
  })
}

export const apiHighVolume = (data: Types.HighVolumeRequest): Promise<IResponse<Types.HighVolumeResult>> => {
  return request.post({
    url: '/data/third/stock/high_volume',
    data
  })  
}

export const apiRiseVolumePrice = (data: Types.RiseVolumePriceRequest): Promise<IResponse<Types.RiseVolumePriceResult>> => {
  return request.post({
    url: '/data/third/stock/rise_volume_price',
    data
  })   
}

export const apiLimitUpPool = (data: Types.LimitUpPoolRequest): Promise<IResponse<Types.LimitUpPoolResult>> => {
  return request.post({
    url: '/data/third/stock/limit_up_pool',
    data
  })   
}
