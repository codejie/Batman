import { defineStore } from 'pinia'

export interface ReportData {
  stock: {
    code: string
    name: string
    type: number
  }
  reports: {
    category: string
    type: string
    arguments: any
    calc?: any
    report?: any[]
  }[]
  dataPeriodStart: string
}

interface ReportDataState {
  dataMap: Record<string, ReportData>
}

export const useTrendStore = defineStore('trend', {
  state: (): ReportDataState => ({
    dataMap: {}
  }),
  actions: {
    setReportData(id: string, data: ReportData) {
      this.dataMap[id] = data
    },
    clearReportData(id: string) {
      delete this.dataMap[id]
    },
    clearAllReportData() {
      this.dataMap = {}
    }
  },
  getters: {
    getReportData: (state) => {
      return (id: string) => state.dataMap[id] || null
    }
  }
})
