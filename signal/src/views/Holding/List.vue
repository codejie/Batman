<script lang="ts">
interface HoldingData {
  id: number
  type: number
  code: string
  name: string
  flag: number
  created: Date
  updated: Date
  quantity: number
  expense: number

  price_avg: number | string
  price_cur?: number
  revenue?: number | string// price_cur * quantity
  profit?: number | string// revenue - expense
  profit_percent?: number | string
}

interface CreateForm {
  type: string
  code: string
}

export interface ViewOptions {
  selected?: HoldingData
}

export const viewOptions = reactive<ViewOptions>({})

</script>

<script setup lang="ts">
import { apiHistory } from '@/api/data'
import { apiCreate, apiRecord } from '@/api/holding'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, reactive, ref } from 'vue'
import { ElDialog, ElButton, ElRow, ElCol, ElInput, ElForm, ElFormItem, ElTable, ElTableColumn } from 'element-plus'

const createDialogVisible = ref<boolean>(false)
const createForm = ref<CreateForm>({
  type: '股票',
  code: ''
})
const data = ref<HoldingData[]>([])

onMounted(() => {
  fetch()
})

async function fetch() {
  const ret = await apiRecord({})
  console.log(ret)
  for (const item of ret.result) {
    const ret_current = await apiHistory({
      type: item.type,
      code: item.code
    })
    const current = ret_current.result[0]
    console.log(current)
    data.value.push({
      id: item.id,
      type: item.type,
      code: item.code,
      name: item.name,
      flag: item.flag,
      created: item.created,
      updated: item.updated,
      quantity: item.quantity,
      expense: item.expense,
      price_avg: (item.expense / item.quantity) || '-',
      price_cur: current.price,
      revenue: current.price * item.quantity,
      profit: current.price * item.quantity - item.expense,
      profit_percent: ((current.price * item.quantity - item.expense) / item.expense) || '-'
    })
  }
}

async function onAdd() {
  const ret = await apiCreate({
    type: createForm.value.type == '股票' ? 1 : 0,
    code: createForm.value.code
  })
  createDialogVisible.value = false
  await fetch()
}

function onOperation(row: HoldingData) {
  console.log(row)
}

</script>

<template>
  <ContentWrap title="持仓">
    <ElRow :gutter="24">
      <ElButton class="my-4 ml-4" type="primary" @click="createDialogVisible=true">增加</ElButton>
    </ElRow>
    <ElRow :gutter="24">
      <ElCol :span="24">
        <ElTable :data=data :stripe="true" :border="true">
          <!-- <ElTableColumn prop="id" label="ID" width="50"></ElTableColumn> -->
            <ElTableColumn type="index" width="40"></ElTableColumn>
          <!-- <ElTableColumn prop="type" label="Type" width="50"></ElTableColumn> -->
          <ElTableColumn prop="code" label="代码" min-width="80"></ElTableColumn>
          <ElTableColumn prop="name" label="名称" min-width="80"></ElTableColumn>
          <!-- <ElTableColumn prop="flag" label="Flag" width="50"></ElTableColumn> -->
          <ElTableColumn prop="quantity" label="数量" min-width="60"></ElTableColumn>
          <ElTableColumn prop="expense" label="费用" min-width="60"></ElTableColumn>
          <ElTableColumn prop="price_avg" label="均价" min-width="80"></ElTableColumn>
          <ElTableColumn prop="price_cur" label="现价" min-width="80"></ElTableColumn>
          <ElTableColumn prop="revenue" label="总价" min-width="80"></ElTableColumn>
          <ElTableColumn prop="profit" label="收益" min-width="80"></ElTableColumn>
          <ElTableColumn prop="profit_percent" label="收益率 %" min-width="100"></ElTableColumn>
          <ElTableColumn prop="created" label="Created" min-width="120"></ElTableColumn>
          <ElTableColumn prop="updated" label="Updated" min-width="120"></ElTableColumn>
          <ElTableColumn label="Action" width="160">
            <template #default="{ row }">
              <ElButton type="text" size="small" @click="onOperation(row)">记录</ElButton>
              <ElButton type="text" size="small" @click="onRemove(row)">删除</ElButton>
            </template>
          </ElTableColumn>
        </ElTable>
      </ElCol>
    </ElRow>
    <ElDialog v-model="createDialogVisible" :destroy-on-close="true" width="25%">
      <template #header>
        <ElText tag="b">新增持股记录</ElText>
      </template>
      <template #default>
        <ElForm :model="createForm" label-position="right" label-width="auto">
          <ElFormItem label="类型">
            <ElInput v-model="createForm.type" :disabled="true" />
          </ElFormItem>
          <ElFormItem label="代码">
            <ElInput v-model="createForm.code" :maxlength="6" />
          </ElFormItem>
        </ElForm>
      </template>
      <template #footer>
        <ElButton @click="createDialogVisible=false">取消</ElButton>
        <ElButton type="primary" @click="onAdd">确定</ElButton>
      </template>      
    </ElDialog>
  </ContentWrap>
</template>