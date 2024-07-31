export type DataFrameSetModel = {
  columns: string[],
  data: any[]
}

// Request & Response
export type NewHighRequest = {
  category: number
}

export type NewHighResponse = DataFrameSetModel