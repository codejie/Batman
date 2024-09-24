<script setup lang="ts">
import ContentWrap from '@/components/ContentWrap/src/ContentWrap.vue';
import { ElRow, ElText } from 'element-plus';
import HoldingTable, { ColumnOpt, ActionOpt} from './components/HoldingTable.vue'
import { onMounted, ref } from 'vue';
import { apiCalcHoldingList } from '@/api/holding';
import { CalcHoldingModel } from '@/api/holding/types';
import { formatToDate } from '@/utils/dateUtil';
import { apiHistory, HistoryDataModel } from '@/api/data/wrap';

const columns: ColumnOpt[] = [
  {
    name: 'code',
    label: '代码',
    width: 90
  },
  {
    name: 'name',
    label: '名称',
    width: 90
  },
  {
    name: 'quantity',
    label: '数量',
    width: 90
  },
  {
    name: 'price',
    label: '现价',
    width: 90
  },
  {
    name: 'value',
    label: '市值', // total price + cost
    width: 120
  },    
  {
    name: 'cost',
    label: '成本', 
    width: 90
  },
  {
    name: 'expense',
    label: '费用', //
    width: 120
  },  
  {
    name: 'gain',
    label: '盈亏', // value + rate
    width: 120
  },
  {
    name: 'updated',
    label: '变动日期', // date + days
    width: 120
  }
]

const actions: ActionOpt[] = [
  {
    name: '详情',
    func: onDetail
  },
  {
    name: '走势',
    func: onTrace
  },  
  {
    name: '交易记录',
    func: onRecord
  },
  {
    name: '设置告警',
    func: onSetReminder
  },
  {
    name: '删除',
    func: onDelete,
    type: 'danger'
  },  
]

const data = ref<any[]>([])

onMounted(async () => {
  await fetch()
  // await fetchAList()
})

async function fetchHistoryData(code: string, type: number): Promise<HistoryDataModel | undefined> {
  const ret = await apiHistory({
    code: code
  }, type)

  if (ret.result.length > 0) {
    return ret.result[0]
  }
  return undefined
}

async function makeData(items: CalcHoldingModel[]) {
  data.value = items
  for (let i = 0; i < data.value.length; ++ i) {
    const item = data.value[i]

    item['cost'] = (item.quantity != 0 ? -(item.expense / item.quantity) : 0.0).toFixed(2)
    item['updated'] = formatToDate(item.updated, 'YYYY-MM-DD')

    const history = await fetchHistoryData(item.code, item.type)
    console.log(history)
    if (history) {
      item['price'] = history.price
      item['value'] = (history.price * item.quantity).toFixed(2)
      item['gain'] = (item.expense + history.price * item.quantity).toFixed(2)
    }
  }
}

async function fetch() {
  const ret = await apiCalcHoldingList({})
  await makeData(ret.result)
}

function onDetail(row: any) {
  console.log(row)
}

function onTrace(row: any) {
  console.log(row)
}

function onRecord(row: any) {
  console.log(row)
}

function onSetReminder(row: any) {
  console.log(row)
}

function onDelete(row: any) {
  console.log(row)
}

</script>
<template>
  <ContentWrap title="持仓列表">
    <ElRow :gutter="24">
      <ElText>abc</ElText>
      Summary
    </ElRow>
    <ElRow :gutter="24">
      <HoldingTable :data="data" :columns="columns" :actions="actions" />
    </ElRow>
  </ContentWrap>
</template>
