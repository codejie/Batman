export interface DbExportRequest {
  flag?: number
}

export type DbExportResult = {
  path: string
  filename: string
  media_type: string
}

export interface DbImportRequest {}
export type DbImportResult = number

export interface DbRemoveAllHistoryDataRequest {}
export type DbRemoveAllHistoryDataResult = number
