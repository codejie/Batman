/*
* K-Line data functions
*/

import { HistoryDataModel } from "@/api/data/stock/types";

export type XData = string[]
export type YData = (number | string)[][]
export type KLineData = {
  data: YData
  max: number
  min: number
}
export type VolumeData = {
  data: YData
  max: number
  min: number
}  
export type MAData = {
  data: YData
  max: number
  min: number
}
export type MADataGroup = { [key in string]: MAData }
export type MACDData = {
  dif: YData
  dea: YData
  macd: YData
  max: number
  min: number
}
export type KLineChartData = {
  xData: XData
  klineData: KLineData
  maData?: MADataGroup
  volumeData: VolumeData
  macdData?: MACDData
}


// function isNumber(n) { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }
export function isNumber(n) { return /^-?[\d.]+(?:e-?\d+)?$/.test(n); }

export function calcMAData(ma: number, xData: XData, kline: KLineData, column: number = 1): MAData {
  const data: YData = []
  for (let i = 0; i < kline.data.length; i++) {
    if (i < ma) {
      data.push([xData[i], Number.NaN])
      continue;
    }
    let sum = 0;
    for (let j = 0; j < ma; j++) {
      sum += (kline.data[i - j][column] as number)// +data[i - j]
    }
    data.push([xData[i], sum / ma])
  }

  return {
    data: data,
    max: (data.reduce((a, b) => a[1] > b[1] ? a : b)[1] as number),
    min: (data.reduce((a, b) => a[1] < b[1] ? a : b)[1] as number)
  }
}

function makeKLineData(history: HistoryDataModel[]): KLineData {
  const data: YData = history.map(({open, close, low, high}) => ([open, close, low, high]))
  return {
    data: data,
    max: (data.reduce((a, b) => a[1] > b[1] ? a : b)[1] as number),
    min: (data.reduce((a, b) => a[1] < b[1] ? a : b)[1] as number)
  }
}

function makeVolumeData(history: HistoryDataModel[]): VolumeData {
  const data: YData = history.map(item => [item.date, item.volume, item.open <= item.close ? 1 : -1])
  return {
    data,
    max: (data.reduce((a, b) => a[1] > b[1] ? a : b)[1] as number),
    min: (data.reduce((a, b) => a[1] < b[1] ? a : b)[1] as number)
  }
}

export function makeKLineChartData(data: HistoryDataModel[]): KLineChartData {
  return {
    xData: data.map(item => item.date),
    klineData: makeKLineData(data),
    volumeData: makeVolumeData(data)
  }  
}

export function makeMACDData(xDate: XData, macdData: any[]): MACDData {
  const dif: YData = []
  const dea: YData = []
  const macd: YData = []

  for (let i: number = 0; i < xDate.length; ++ i) {
    dif.push([xDate[i], macdData[i][0]]),// (isNumber(macdData[i][0]) ? parseFloat(macdData[i][0]).toFixed(2) : macdData[i][0])])
    dea.push([xDate[i], macdData[i][1]]), //(isNumber(macdData[i][1]) ? parseFloat(macdData[i][1]).toFixed(2) : macdData[i][1])])
    macd.push([xDate[i], macdData[i][2], macdData[i][2] >= 0 ? 1 : -1]) //(isNumber(macdData[i][2]) ? parseFloat(macdData[i][2]).toFixed(2) : macdData[i][2]), macdData[i][2] >= 0 ? 1 : -1]);
  }
  return {
    dif,
    dea,
    macd,
    max: (dif.reduce((a, b) => a[1] > b[1] ? a : b)[1] as number),
    min: (dif.reduce((a, b) => a[1] < b[1] ? a : b)[1] as number)
  }
}

export function makeMADataGroup(ma: number[], chartData: KLineChartData): MADataGroup {
  const ret: MADataGroup = {}
  ma.forEach(item => {
    ret[item] = calcMAData(item, chartData.xData, chartData.klineData)
  })
  return ret
}

export function fitKLineData(data: KLineData, base: KLineData): KLineData {
  const arg1 = (base.max - base.min) / (data.max - data.min)
  const arg2 = arg1 * data.min - base.min
  
  return {
    data: data.data.map(item => [
      ((item[0] as number) * arg1 - arg2),
      ((item[1] as number) * arg1 - arg2),
      ((item[2] as number) * arg1 - arg2),
      ((item[3] as number) * arg1 - arg2)
    ]),
    max: data.max,
    min: data.min
  }
}

export function fitMAData(data: MAData, base: MAData): MAData {
  // console.log(data)
  // console.log(base)
  const arg1 = (base.max - base.min) / (data.max - data.min)
  // console.log(`arg1 = ${arg1}`)
  const arg2 = arg1 * data.min - base.min
  // console.log(`arg2 = ${arg2}`)
  return {
    data: data.data.map(item => [item[0], ((item[1] as number) * arg1 - arg2)]),
    max: data.max,
    min: data.min
  }
}

export function fitVolumeData(data: VolumeData, base: VolumeData): VolumeData {
  const diff = base.max - base.min
  const arg1 = diff / (data.max - data.min)
  const arg2 = arg1 * data.min - base.min
  return {
    data: data.data.map(item => [item[0], ((item[1] as number) * arg1 - arg2), item[2]]),
    max: data.max,
    min: data.min
  }
}

export function fitMACDData(data: MACDData, base: MACDData): MACDData {
  const arg1 = (base.max - base.min) / (data.max - data.min)
  const arg2 = arg1 * data.min - base.min

  return {
    dif: data.dif.map(item => [item[0], ((item[1] as number) * arg1 - arg2)]),
    dea: data.dea.map(item => [item[0], ((item[1] as number) * arg1 - arg2)]),
    macd: data.macd.map(item => [item[0], ((item[1] as number) * arg1 - arg2), item[2]]),
    max: data.max,
    min: data.min
  }
}
