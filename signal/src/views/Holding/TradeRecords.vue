<script setup lang="ts">
import ContentWrap from '@/components/ContentWrap/src/ContentWrap.vue';
import { ElMessage, ElMessageBox, ElRow, ElSelect, ElOption, ElButton } from 'element-plus';
import HoldingTable, { ActionOpt, ColumnOpt } from './components/HoldingTable.vue';
import { onMounted, ref } from 'vue';
import { apiGetHoldingRecord, apiRemoveRecord } from '@/api/holding';
import { HoldingRecordModel } from '@/api/holding/types';

const columns: ColumnOpt[] = [
  {
    name: 'action',
    label: '操作',
    width: 90
  },  
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
    width: 80
  },   
  {
    name: 'expense',
    label: '费用', //
    width: 100
  },  
  {
    name: 'days',
    label: '持有',
    width: 70
  },
  {
    name: 'updated',
    label: '变动日期',
    width: 120
  }
]

const actions: ActionOpt[] = [
  {
    name: '删除',
    func: onDelete,
    type: 'danger'
  },  
]

const codeList = ref<any[]>([])
const codeSelected = ref<any>()
const data = ref<any[]>([])

function makeCodeList(items: HoldingRecordModel[]) {
  codeList.value = [
    {
      id: -1,
      value: {holding: -1, type: -1, code: '-1'},
      label: 'All'
    }
  ]
  items.forEach(item => {
    if (!codeList.value.find(i => item.holding == i.value.holding)) { // (i.value.code == item.code && i.value.type == item.type))) {
      codeList.value.push({
        id: item.id,
        value: {
          holding: item.holding,
          type: item.type,
          code: item.code
        },
        label: `${item.code}(${item.name})`
      })
    }
  })
}

function makeData(items: HoldingRecordModel[]) {
  data.value = []
  items.forEach(item => {
    data.value.push({
      id: item.id,
      type: item.type,
      code: item.code,
      name: item.name,
      action: item.action == 0 ? '买入' : '卖出',
      quantity: item.quantity,
      expense: item.expense,
      days: `${Math.floor((Date.parse(item.updated) - Date.parse(item.created)) / 86400000)}天`,
      created: item.created,
      updated: item.updated,
      flag: item.flag      
    })
  })
}

async function fetch(type?: number, code?: string) {
  const ret = await apiGetHoldingRecord({
    type: type,
    code: code
  })
  makeData(ret.result)
  return ret.result
}

onMounted(async () => {
  const result = await fetch()
  makeCodeList(result)
})

async function onDelete(row: any) {
  // console.log(row)
  try {
    await ElMessageBox.confirm(
      `remove holding record '${row.id}'?`,
      'Warning', 
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const r = await apiRemoveRecord({
      id: row.id
    })
    if (r.code == 0) {
      ElMessage({
        type: 'success',
        message: 'holding record be removed.'
      })
    } else {
      ElMessage({
        type: 'error',
        message: 'removing holding record failed.'
      })
    }
    await fetch()
  } catch (error) {

  }
}

async function onCodeChanged(value) {
  if (value.value.holding == -1) {
    await fetch()
  } else {
    await fetch(value.value.type, value.value.code)
  }
}

</script>
<template>
  <ContentWrap title="交易记录">
    <ElRow :gutter="24" style="margin-bottom: 8px;">
      <ElSelect v-model="codeSelected" style="width: 220px;" @change="onCodeChanged">
        <ElOption v-for="item in codeList" :key="item.id" :label="item.label" :value="item" />
      </ElSelect>
      <!-- <ElButton style="margin-left: 4px;">Select</ElButton> -->
    </ElRow>
    <ElRow :gutter="24">
      <HoldingTable :data="data" :columns="columns" :actions="actions" />
    </ElRow>
  </ContentWrap>
</template>
