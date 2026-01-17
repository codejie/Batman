export const tools = [ 
  {
    name: 'get_weather',
    description: '获取指定城市的当前天气',
    handler: get_weather,
    parameters: {
      type: 'object',
      properties: {
        location: { type: 'string', description: '城市名称，如：北京, 上海' },
        unit: { type: 'string', enum: ['celsius', 'fahrenheit'] }
      },
      required: ['location']
    },
    enabled: true
  },
  {
    name: 'get_stock_price',
    description: '获取股票当前价格',
    handler: get_stock_price,
    parameters: {
      type: 'object',
      properties: {
        symbol: { type: 'string', description: '股票代码，如：AAPL, 000001.SZ' }
      },
      required: ['symbol']
    },
    enabled: true
  } 
]

function get_weather(args: any) {
  console.log('Tool Call: get_weather', args)
  // 模拟 API 调用
  return {
    location: args.location,
    temperature: Math.floor(Math.random() * 30),
    condition: ['晴朗', '多云', '阴', '小雨'][Math.floor(Math.random() * 4)],
    humidity: '45%'
  }
}

function get_stock_price(args: any) {
  console.log('Tool Call: get_stock_price', args)
  // 模拟 API 调用
  return {
    symbol: args.symbol,
    price: (Math.random() * 500 + 100).toFixed(2),
    change: (Math.random() * 10 - 5).toFixed(2) + '%',
    last_updated: new Date().toLocaleString()
  }
}
