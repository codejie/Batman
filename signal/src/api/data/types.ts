export const TYPE_INDEX: number = 1
export const TYPE_STOCK: number = 2
export const TYPE_FUND: number = 3

export const FUND_TYPE_OPEN: number = 0
export const FUND_TYPE_ETF: number = 1
export const FUND_TYPE_LOF: number = 2
const ETF_CODE_PREFIXES = [
  '159',
  '510',
  '511',
  '512',
  '513',
  '515',
  '516',
  '517',
  '518',
  '560',
  '561',
  '562',
  '563',
  '588',
  '589'
]
const LOF_CODE_PREFIXES = [
  '160',
  '161',
  '162',
  '163',
  '164',
  '165',
  '166',
  '167',
  '168',
  '169',
  '501',
  '502'
]

export type ItemTypeLabel = '股票' | '指数' | '基金' | 'ETF' | 'LOF'
export const ITEM_TYPE_OPTIONS: ItemTypeLabel[] = ['股票', '指数', 'ETF', 'LOF', '基金']

export function normalizeFundMarket(market?: number | string | null): number | undefined {
  if (market === undefined || market === null || market === '') return undefined
  const value = Number(market)
  return Number.isNaN(value) ? undefined : value
}

export function inferFundMarketByCode(code?: string): number | undefined {
  if (!code) return undefined
  if (ETF_CODE_PREFIXES.some((prefix) => code.startsWith(prefix))) return FUND_TYPE_ETF
  if (LOF_CODE_PREFIXES.some((prefix) => code.startsWith(prefix))) return FUND_TYPE_LOF
  return undefined
}

export function resolveFundMarket(
  market?: number | string | null,
  code?: string
): number | undefined {
  const codeMarket = inferFundMarketByCode(code)
  const normalizedMarket = normalizeFundMarket(market)
  if (
    normalizedMarket === FUND_TYPE_OPEN &&
    (codeMarket === FUND_TYPE_ETF || codeMarket === FUND_TYPE_LOF)
  ) {
    return codeMarket
  }
  return normalizedMarket ?? codeMarket
}

export function getItemTypeLabel(
  type: number,
  market?: number | string | null,
  code?: string
): ItemTypeLabel {
  if (type === TYPE_STOCK) return '股票'
  if (type === TYPE_INDEX) return '指数'
  if (type === TYPE_FUND) {
    const fundMarket = resolveFundMarket(market, code)
    if (fundMarket === FUND_TYPE_ETF) return 'ETF'
    if (fundMarket === FUND_TYPE_LOF) return 'LOF'
    return '基金'
  }
  return '基金'
}

export function getItemRequestType(label: string): number {
  return label === '股票' ? TYPE_STOCK : label === '指数' ? TYPE_INDEX : TYPE_FUND
}

export function getItemFundMarket(label: string): number | undefined {
  if (label === 'ETF') return FUND_TYPE_ETF
  if (label === 'LOF') return FUND_TYPE_LOF
  if (label === '基金') return FUND_TYPE_OPEN
  return undefined
}

export function isMatchedItemType(
  label: string,
  item: { type: number; market?: number | string | null; code?: string }
): boolean {
  if (item.type !== getItemRequestType(label)) return false
  if (item.type !== TYPE_FUND) return true

  const expectedMarket = getItemFundMarket(label)
  const actualMarket = resolveFundMarket(item.market, item.code)
  if (expectedMarket === FUND_TYPE_OPEN && actualMarket === undefined) return true
  return expectedMarket === undefined || actualMarket === expectedMarket
}

export const PERIOD_DAILY: string = 'daily'
export const PERIOD_WEEKLY: string = 'weekly'
export const PERIOD_MONTHLY: string = 'monthly'

export const ADJUST_QFQ: string = 'qfq'

export const RECORD_FLAG_NORMAL: number = 0
export const RECORD_FLAG_DISABLED: number = 1

export interface DownloadListRequest {
  type: number
}
export type DownloadListResult = void

export interface HistoryDataItem {
  日期: string
  开盘: number
  收盘: number
  最高: number
  最低: number
  成交量: number
  成交额: number
  振幅: number
  涨跌幅: number
  涨跌额: number
  换手率: number
}

export interface SpotDataItem {
  序号: number
  代码: string
  名称: string
  最新价: number
  涨跌幅: number
  涨跌额: number
  成交量: number
  成交额: number
  振幅: number
  最高: number
  最低: number
  今开: number
  昨收: number
  量比?: number
  换手率?: number
  市盈率?: number
  市净率?: number
  总市值?: number
  流通市值?: number
  涨速?: number
  涨跌5分钟?: number
  涨跌幅60日?: number
  年初至今涨跌幅?: number
}

export interface GetLatestHistoryDataRequest {
  type: number
  code: string
  period?: string
  adjust?: string
  limit?: number // default 1
  record_flag?: number
}
export type GetLatestHistoryDataResult = HistoryDataItem | HistoryDataItem[] | undefined

export interface GetHistoryDataRequest {
  type: number
  code: string
  start?: string
  end?: string
  period?: string
  adjust?: string
  limit?: number
  record_flag?: number
}
export type GetHistoryDataResult = HistoryDataItem[]

export interface GetSpotDataRequest {
  type: number
  codes?: string[]
  useHistory?: boolean
}
export type GetSpotDataResult = SpotDataItem[]

export interface GetNameRequest {
  type: number
  code: string
}
export type GetNameResult = string

export interface GetItemInfoRequest {
  type: number
  key: string
}
export interface ItemInfo {
  type: number
  code: string
  name: string
  market?: number | string
}
export type GetItemInfoResult = ItemInfo
