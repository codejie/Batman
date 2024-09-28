/**
 * Independent time operation tool to facilitate subsequent switch to dayjs
 */
import dayjs from 'dayjs'
// import utc from 'dayjs/plugin/utc'
// import timezone from 'dayjs/plugin/timezone'

// dayjs.extend(utc)
// dayjs.extend(timezone)
// dayjs.tz.setDefault('Asia/Shanghai')

const DATE_TIME_FORMAT = 'YYYY-MM-DD HH:mm:ss'
const DATE_FORMAT = 'YYYY-MM-DD'

export function formatToDateTime(date?: dayjs.ConfigType, format = DATE_TIME_FORMAT): string {
  return dayjs(date).format(format)
}

export function formatToDate(date?: dayjs.ConfigType, format = DATE_FORMAT): string {
  return dayjs(date).format(format)
}

export const dateUtil = dayjs
