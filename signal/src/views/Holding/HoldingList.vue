<script setup lang="ts">
import ContentWrap from '@/components/ContentWrap/src/ContentWrap.vue';
import { ElDialog, ElRow, ElText, ElButton } from 'element-plus';
import HoldingTable, { ColumnOpt, ActionOpt} from './components/HoldingTable.vue'
import { onMounted, ref } from 'vue';
import { apiCalcHoldingList } from '@/api/holding';
import { CalcHoldingModel } from '@/api/holding/types';
import { formatToDate } from '@/utils/dateUtil';
import { apiHistory, HistoryDataModel } from '@/api/data/wrap';
import TradeTraceForm from './components/TradeTraceForm.vue';
import { ReqParam } from '@/components/KLine';
import CreateHoldingForm from './components/CreateHoldingForm.vue';

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
    width: 150
  },
  {
    name: 'days',
    label: '持有',
    width: 80
  },
  {
    name: 'updated',
    label: '变动日期', // date + days
    width: 200
  }
]

const actions: ActionOpt[] = [
  {
    name: '操作',
    func: onAction
  },
  {
    name: '交易走势',
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
const tradeDialogVisible = ref<boolean>(false)
const createDialogVisible = ref<boolean>(false)
const reqParam = ref<ReqParam>()
const reqHolding = ref<number>()
const reqTitle = ref<string>('')

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
    item['days'] = `${Math.floor((Date.parse(item.updated) - Date.parse(item.created)) / 86400000)}天`
    item['updated'] = formatToDate(item.updated, 'YYYY-MM-DD')

    const history = await fetchHistoryData(item.code, item.type)
    if (history) {
      item['price'] = history.price
      const value = history.price * item.quantity
      item['value'] = value.toFixed(2)
      const gain = item.expense + history.price * item.quantity
      item['gain'] = `${gain.toFixed(2)} [${(gain * 100 /value).toFixed(2)}%]`  // (item.expense + history.price * item.quantity).toFixed(2)
    }
  }
}

async function fetch() {
  const ret = await apiCalcHoldingList({})
  await makeData(ret.result)
}

function onCreateClick() {
  createDialogVisible.value = true
}

function onAction(row: any) {
  console.log(row)
}

function onRecord(row: any) {
  reqTitle.value = `${row.code}(${row.name}) [数量: ${row.quantity} | 费用: ${row.value} | 盈亏: ${row.gain}]`
  reqParam.value = {
    type: row.type,
    code: row.code,
    name: row.name,
  }
  reqHolding.value = row.id
  tradeDialogVisible.value = true
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
      <ElButton class="padding" type="primary" @click="onCreateClick">新增</ElButton>
    </ElRow>
    <ElRow :gutter="24">
      <HoldingTable :data="data" :columns="columns" :actions="actions" />
    </ElRow>
    <ElDialog v-model="tradeDialogVisible" :destroy-on-close="true">
      <template #header>
        <ElText tag="b">{{ reqTitle }}</ElText>
      </template>
      <TradeTraceForm :req-param="reqParam!" :holding="reqHolding!" />
      <template #footer>
        <ElButton type="primary" @click="tradeDialogVisible=false">Close</ElButton>
      </template>    
    </ElDialog>
    <ElDialog v-model="createDialogVisible" :destroy-on-close="true" width="25%">
      <template #header>
        <ElText tag="b">新增</ElText>
      </template>      
      <CreateHoldingForm />
      <template #footer>
        <ElButton type="primary" @click="createDialogVisible=false">Close</ElButton>
      </template>         
    </ElDialog>
  </ContentWrap>
</template>
<style lang="css">
.padding {
  margin: 8px;
}
</style>
