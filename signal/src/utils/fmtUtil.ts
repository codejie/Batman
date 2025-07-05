export function getTypeCodeString(type: number, code: string): string {
  return `${type}_${code}`
}

export function formatNumberString(value?: number): string {
  if (value === undefined || value === null || isNaN(value)) {
    return '-'
  }
  return value.toFixed(2)
}

export function formatRateString(value?: number): string {
  if (value === undefined || value === null || isNaN(value)) {
    return '-'
  }
  return (value * 100).toFixed(2) + '%'
}

export function formatRateString2(value1?: number, value2?: number): string {
  if (value1 === undefined || value1 === null || isNaN(value1)) {
    return '-'
  }
  if (value2 === undefined || value2 === null || isNaN(value2)) {
    return '-'
  }  

  return (value1 / value2 * 100).toFixed(2) + '%'
}