import { apiGetHistoryData, apiGetName, apiGetItemInfo } from '@/api/data'

export const tools = [
  {
    name: 'apiGetHistoryData',
    description: '获取历史数据',
    handler: apiGetHistoryData,
    parameters: {
      type: 'object',
      properties: {
        type: { type: 'number', description: '数据类型' },
        code: { type: 'string', description: '股票代码' },
        start: { type: 'string', description: '开始时间，格式：YYYY-MM-DD' },
        end: { type: 'string', description: '结束时间，格式：YYYY-MM-DD' },
        period: { type: 'string', description: '时间周期，默认值：daily，可选值：daily, weekly, monthly' },
        adjust: { type: 'string', description: '复权方式，默认值：qfq，可选值：qfq, hfq' },
        limit: { type: 'number', description: '限制数量' },
        record_flag: { type: 'number', description: '记录标志，默认值：0，可选值：0, 1' }
      },
      required: ['type', 'code']
    },
    enabled: true
  },
  {
    name: 'apiGetName',
    description: '获取股票名称',
    handler: apiGetName,
    parameters: {
      type: 'object',
      properties: {
        type: { type: 'number', description: '数据类型' },
        code: { type: 'string', description: '股票代码' }
      },
      required: ['type', 'code']
    },
    enabled: true
  },
  {
    name: 'apiGetItemInfo',
    description: '获取股票信息',
    handler: apiGetItemInfo,
    parameters: {
      type: 'object',
      properties: {
        type: { type: 'number', description: '数据类型' },
        key: { type: 'string', description: '股票名称或股票代码' }
      },
      required: ['type', 'key']
    },
    enabled: true
  },
  {
    name: 'get_type',
    description: '获取数据类型',
    handler: get_type,
    parameters: {
      type: 'object',
      properties: {
        category: { type: 'string', description: '数据类型' }
      },
      required: ['category']
    },
    enabled: true
  }
]

function get_type(category: string) {
  return category === '指数' ? 1 : 2
}
