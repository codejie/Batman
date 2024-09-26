<script setup lang="ts">
import { apiHistory, HistoryDataModel } from '@/api/data/wrap';
import { apiGetRecordList } from '@/api/holding';
import { RecordModel } from '@/api/holding/types';
import { ReqParam } from '@/components/KLine';
import { formatToDate } from '@/utils/dateUtil';
import { ElRow, ElTable, ElTableColumn } from 'element-plus'
import { onMounted, PropType, ref } from 'vue';
import TradeKLineForm from './TradeKLineForm.vue';

const EXTEND_MONTHS: number = 2

export type TradeRecord = {
  id: number
  holding: number
  action: string
  quantity: number
  price: number | string // 现价
  cost: number | string // 成本
  expense: number
  comment?: string
  created: string
}

const props = defineProps({
  holding: {
    type: Number,
    required: true
  },
  reqParam: {
    type: Object as PropType<ReqParam>,
    required: true
  }
})
let start: Date = new Date('9999/01/01')
let end: Date = new Date('0001/01/01')

const historyData = ref<HistoryDataModel[]>([])
const tradeRecords = ref<TradeRecord[]>([])

function makeTradeRecords(data: RecordModel[]) {
  data.forEach(item => {
    tradeRecords.value.push({
      id: item.id,
      holding: item.holding,
      action: item.action == 0 ? '买入' : '卖出',
      quantity: item.quantity,
      price: '-',
      cost: (item.expense / item.quantity).toFixed(2),
      expense: item.expense,
      comment: item.comment,
      created: formatToDate(item.created, 'YYYY-MM-DD')
    })
    const c = new Date(item.created)
    if (start > c) start = c
    if (end < c) end = c
  })
}

function updateTradeRecord(data: HistoryDataModel[]) {
  tradeRecords.value.forEach(item => {
    const d = data.find(i => i.date == item.created)
    if (d) {
      item.price = d.price
    }
  })
} 

onMounted(async () => {
  const retRecord = await apiGetRecordList({
    holding: props.holding
  })
  makeTradeRecords(retRecord.result)

  const s = start.setMonth(start.getMonth() - EXTEND_MONTHS)
  const e = end.setMonth(end.getMonth() + EXTEND_MONTHS)

  const retHistory = await apiHistory({
    code: props.reqParam.code,
    start: formatToDate(s, 'YYYY-MM-DD'),
    end: formatToDate(e, 'YYYY-MM-DD')
  }, props.reqParam.type)
  historyData.value = retHistory.result
  updateTradeRecord(retHistory.result)
})

</script>
<template>
  <ElRow :gutter="24">
    <TradeKLineForm :history="historyData" :records="tradeRecords" />
  </ElRow>
  <ElRow :gutter="24">
    <ElTable :data="tradeRecords" size="small" :border="true" max-height="200" >
      <ElTableColumn type="index" width="35" />
      <ElTableColumn prop="action" label="操作" width="45" />
      <ElTableColumn prop="quantity" label="数量" width="80" />
      <ElTableColumn prop="price" label="价格" width="70" />
      <ElTableColumn prop="cost" label="成本"  width="70" />
      <ElTableColumn prop="expense" label="费用" width="90" />
      <ElTableColumn prop="created" label="交易日期" width="120" />      
      <ElTableColumn prop="comment" label="备注"  />
    </ElTable>
  </ElRow>
</template>