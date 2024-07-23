import KLinePanel from './src/KLinePanel.vue'
import KLinePanel2 from './src/KLinePanel2.vue'

export { KLinePanel, KLinePanel2 }

export type DataParam = {
  code: string,
  start: string,
  end: string,
  period?: string,
  adjust?: string
}

export type ShowParam = {
  maLines?: number[],
  markLines?: boolean,
  hideVolume?: boolean,  
  hideKLine?: boolean
}