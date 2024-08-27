/*
* K-Line data functions
*/

import { HistoryDataModel } from "@/api/data/stock/types";

export type XData = string[]
export type KLineData = (number | string)[][]
export type VolumeData = (number | string)[][]
export type KLineChartData = {
  xData: XData
  klineData: KLineData
  volumeData: VolumeData 
}
export type MAData = (number | string)[][]
export type MACDData = {
  dif: (number | string)[][]
  dea: (number | string)[][]
  macd: (number| string)[][]  
}

// function isNumber(n) { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }
export function isNumber(n) { return /^-?[\d.]+(?:e-?\d+)?$/.test(n); }

export function calcMAData(ma: number, xData: XData, kline: KLineData, column: string = 'close'): MAData {
  const ret: MAData = []
  for (let i = 0; i < kline.length; i++) {
    if (i < ma) {
      ret.push([xData[i], '-'])
      continue;
    }
    let sum = 0;
    for (let j = 0; j < ma; j++) {
      sum += kline[i - j][column] // +data[i - j]
    }
    ret.push([xData[i], (sum / ma).toFixed(2)])
  }
  return ret  
}

export function makeKLineChartData(data: HistoryDataModel[]): KLineChartData {
  return {
    xData: data.map(item => item.date),
    klineData: data.map(({open, close, low, high}) => ([open, close, low, high])),
    volumeData: data.map(item => [item.date, item.volume, item.open <= item.close ? 1 : -1])    
  }  
}

export function makeMACDData(xDate: XData, macd: any[]): MACDData {
  const ret: MACDData  = {
    dif: [],
    dea: [],
    macd: []
  }
  for (let i: number = 0; i < xDate.length; ++ i) {
    ret.dif.push([xDate[i], (isNumber(macd[i][0]) ? parseFloat(macd[i][0]).toFixed(2) : macd[i][0])])
    ret.dea.push([xDate[i], (isNumber(macd[i][1]) ? parseFloat(macd[i][1]).toFixed(2) : macd[i][1])])
    ret.macd.push([xDate[i], (isNumber(macd[i][2]) ? parseFloat(macd[i][2]).toFixed(2) : macd[i][2]), macd[i][2] >= 0 ? 1 : -1]);
  }
  return ret
}