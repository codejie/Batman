import request from '@/axios'
import { HighVolumeRequest, HighVolumeResponse, LimitUpPoolRequest, LimitUpPoolResponse, NewHighRequest, NewHighResponse, RiseVolumePriceRequest, RiseVolumePriceResponse, UptrendRequest, UptrendResponse } from './types'

export const apiNewHigh = (data: NewHighRequest): Promise<Response<NewHighResponse>> => {
  return request.post({
    url: '/data/third/stock/new_high',
    data
  })
}

export const apiUptrend = (data: UptrendRequest): Promise<Response<UptrendResponse>> => {
  return request.post({
    url: '/data/third/stock/uptrend',
    data
  })
}

export const apiHighVolume = (data: HighVolumeRequest): Promise<Response<HighVolumeResponse>> => {
  return request.post({
    url: '/data/third/stock/high_volume',
    data
  })  
}

export const apiRiseVolumePrice = (data: RiseVolumePriceRequest): Promise<Response<RiseVolumePriceResponse>> => {
  return request.post({
    url: '/data/third/stock/rise_volume_price',
    data
  })   
}

export const apiLimitUpPool = (data: LimitUpPoolRequest): Promise<Response<LimitUpPoolResponse>> => {
  return request.post({
    url: '/data/third/stock/limit_up_pool',
    data
  })   
}
