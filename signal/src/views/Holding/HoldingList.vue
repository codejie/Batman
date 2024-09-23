<script setup lang="ts">
import ContentWrap from '@/components/ContentWrap/src/ContentWrap.vue';
import { ElRow, ElText } from 'element-plus';
import HoldingTable, { ColumnOpt, ActionOpt} from './components/HoldingTable.vue'
import { ref } from 'vue';

// type ColumnOpt = {
//   name: string,
//   width: number
// }

// type OperationOpt = {
//   name: string,
//   func: Function
// }

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
    name: 'cost',
    label: '成本',
    width: 90
  },
  {
    name: 'value',
    label: '市值', // total price + cost
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

const data = ref<any[]>([
  {
    type: 1,
    code: '000001',
    name: 'aaa',
    quantity: 100
  }
])

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
