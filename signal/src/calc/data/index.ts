export function calcMAData(ma: number, data: number[]): string[] {
  const result: string[] = []
  for (let i = 0, len = data.length; i < len; i++) {
    if (i < ma) {
      result.push('-')
      continue
    }
    let sum = 0
    for (let j = 0; j < ma; j++) {
      sum += +data[i - j]
    }
    result.push((sum / ma).toFixed(2))
  }
  return result
}
