<script setup lang="ts">
import { apiHistory, HistoryDataModel } from '@/api/data/wrap';
import { apiGetRecordList } from '@/api/holding';
import { RecordModel } from '@/api/holding/types';
import { ReqParam } from '@/components/KLine';
import { formatToDate } from '@/utils/dateUtil';
import { ElRow, ElTable, ElTableColumn } from 'element-plus'
import { onMounted, PropType, ref } from 'vue';

type TradeRecord = {
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

const tradeRecords = ref<TradeRecord[]>([])

function makeTradeRecords(data: RecordModel[]) {
  data.forEach(item => {
    tradeRecords.value.push({
      id: item.id,
      holding: item.holding,
      action: item.action == 0 ? 'Buy' : 'Sell',
      quantity: item.quantity,
      price: '-',
      cost: (item.expense / item.quantity).toFixed(2),
      expense: item.expense,
      comment: item.comment,
      created: formatToDate(item.created, 'YYYY-MM-DD')
    })
    console.log(new Date(item.created))
    console.log(start > new Date(item.created))
    const c = new Date(item.created)
    if (start > c) start = c
    if (end < c) end = c
  })
  console.log(start)
  console.log(end)
}

function updateTradeRecord(data: HistoryDataModel[]) {
  tradeRecords.value.forEach(item => {
    const d = data.find(i => i.date == item.created)
    if (d) {
      item.price = d.price
    }
  })
  console.log(tradeRecords.value)
} 

onMounted(async () => {
  const retRecord = await apiGetRecordList({
    holding: props.holding
  })
  makeTradeRecords(retRecord.result)

  const retHistory = await apiHistory({
    code: props.reqParam.code,
    start: formatToDate(start, 'YYYY-MM-DD'),
    end: formatToDate(end, 'YYYY-MM-DD')
  }, props.reqParam.type)
  console.log(retHistory.result)
  updateTradeRecord(retHistory.result)
})

</script>
<template>
  <ElRow :gutter="24">
    <ElTable :data="tradeRecords">
      <ElTableColumn prop="action" label="操作" />
      <ElTableColumn prop="quantity" label="数量" />
      <ElTableColumn prop="price" label="价格" />
    </ElTable>
  </ElRow>
</template>