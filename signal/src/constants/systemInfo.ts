const formatDateTime = (value: string) => {
  if (!value || value === 'unknown') {
    return 'unknown'
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString('zh-CN', {
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

export const systemInfo = {
  name: __SYSTEM_NAME__,
  version: __SYSTEM_VERSION__,
  gitCommit: __SYSTEM_GIT_COMMIT__,
  buildTime: formatDateTime(__SYSTEM_BUILD_TIME__)
}
