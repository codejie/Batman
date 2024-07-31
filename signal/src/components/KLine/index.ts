import KLinePanel from './src/KLinePanel.vue'
import KLinePanel2 from './src/KLinePanel2.vue'
import KLinePanel3 from './src/KLinePanel3.vue'
import KLinePanel4 from './src/KLinePanel4.vue'

export { KLinePanel, KLinePanel2, KLinePanel3, KLinePanel4 }

export type DataParam = {
  code: string,
  start?: string,
  end?: string,
  period?: string,
  adjust?: string
}

export type ShowParam = {
  maLines?: number[],
  markLines?: boolean,
  hideVolume?: boolean,  
  hideKLine?: boolean
}