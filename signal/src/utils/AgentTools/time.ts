export const tools = [
  {
    name: 'get_date',
    description: '获取当前日期',
    handler: () => {
      return new Date().toISOString().split('T')[0]
    },
    parameters: {
      type: 'object',
      properties: {},
      required: []
    },
    enabled: true
  },
  {
    name: 'get_time',
    description: '获取当前时间',
    handler: () => {
      return new Date().toTimeString().split(' ')[0]
    },
    parameters: {
      type: 'object',
      properties: {},
      required: []
    },
    enabled: true
  },
  {
    name: 'get_datetime',
    description: '获取当前日期和时间，本地时区为UTC+8，转换为本地时间输出',
    handler: () => {
      return new Date().toISOString()
    },
    parameters: {
      type: 'object',
      properties: {},
      required: []
    },
    enabled: true
  }
]