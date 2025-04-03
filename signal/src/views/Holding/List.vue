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
  price_cur?: number | string
  revenue?: number | string// price_cur * quantity
  profit?: number | string// revenue - expense
  profit_percent?: number | string
}

interface OperationData {
  id: number
  holding: number
  action: number
  quantity: number
  price: number
  expense: number
  comment?: string
  created: Date
}

interface HoldingOperationData {
  holding: HoldingData
  items: OperationData[]
}

interface CreateForm {
  type: string
  code: string
}

interface OperationForm {
  holding: number
  type: number
  code: string
  name: string
  action: number
  quantity: number
  price: number
  expense: number
  comment?: string    
}

async function getHoldingData(id?: number, type?: number, code?: string, flag?: number): Promise<HoldingData[]> {
  const results: HoldingData[] = []
  const ret = await apiRecord({
    id,
    type,
    code,
    flag
  })
  for (const item of ret.result) {
    const ret_current = await apiGetLatestHistoryData({
      type: item.type,
      code: item.code
    })
    const price = ret_current.result ? ret_current.result.收盘 : undefined
    console.log(price)
    const avg = (-item.expense / item.quantity) || undefined
    const precent = price ? ((price * item.quantity + item.expense) / -item.expense) : undefined
    const profit = price ? (price * item.quantity + item.expense) : undefined
    results.push({
      id: item.id,
      type: item.type,
      code: item.code,
      name: item.name,
      flag: item.flag,
      created: item.created,
      updated: item.updated,
      quantity: item.quantity,
      expense: item.expense,
      price_avg: avg ? avg.toFixed(2) : '-',
      price_cur: price || '-',
      revenue: price ? price * item.quantity : '-',
      profit: profit || '-',
      profit_percent: precent ? ((precent * 100).toFixed(2) + '%') : '-'
    })
  }
  return results
}

</script>

<script setup lang="ts">
import { apiGetLatestHistoryData } from '@/api/data'
import { apiCreate, apiFlag, apiOperationCreate, apiOperationList, apiOperationRemove, apiRecord } from '@/api/holding'
import { HOLDING_FLAG_REMOVED, OPERATION_ACTION_BUY, OPERATION_ACTION_SELL } from '@/api/holding/types'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref } from 'vue'
import {
  ElText, ElDialog, ElButton, ElRow, ElCol, ElInput, ElForm, ElFormItem, ElTable, ElTableColumn,
  ElRadioGroup, ElRadioButton
 } from 'element-plus'
import { formatToDate, formatToDateTime } from '@/utils/dateUtil'
import { TYPE_INDEX, TYPE_STOCK } from '@/api/data/types'

const createDialogVisible = ref<boolean>(false)
const operationDialogVisible = ref<boolean>(false)
const createForm = ref<CreateForm>({
  type: '股票',
  code: ''
})
const operationForm = ref<OperationForm>({
  holding: 0,
  type: TYPE_STOCK,
  code: '',
  name: '',
  action: OPERATION_ACTION_BUY,
  quantity: 0,
  price: 0,
  expense: 0,
  comment: ''
})
const data = ref<HoldingOperationData[]>([])
const expandRows = ref<string[]>([])

async function fetchHoldingData() {
  data.value = []
  const holding = await getHoldingData()
  for (const item of holding) {
    data.value.push({
      holding: item,
      items: []
    })
  }

  const ret = await apiOperationList({})

  for (const item of ret.result) {
    const holding = data.value.find((x) => x.holding.id === item.holding)
    holding!.items.push(item)
  }
}

onMounted(async () => {
  await fetchHoldingData()
})

async function onAdd() {
  const ret = await apiCreate({
    type: createForm.value.type == '股票' ? TYPE_STOCK : TYPE_INDEX,
    code: createForm.value.code
  })
  createDialogVisible.value = false
  await fetchHoldingData()
}

function onOperation(row: HoldingOperationData) {
  operationForm.value.holding = row.holding.id
  operationForm.value.type = row.holding.type
  operationForm.value.code = row.holding.code
  operationForm.value.name = row.holding.name
  operationDialogVisible.value = true
}

function onPriceBlur() {
  operationForm.value.expense = operationForm.value.quantity * operationForm.value.price
}

function onQuantityBlur() {
  operationForm.value.expense = operationForm.value.quantity * operationForm.value.price
}

async function onAddOperation() {
  console.log(operationForm.value)
  const ret = await apiOperationCreate({
    holding: operationForm.value.holding,
    action: operationForm.value.action,
    quantity: operationForm.value.quantity,
    price: operationForm.value.price,
    expense: operationForm.value.expense,
    comment: operationForm.value.comment
  })
  operationDialogVisible.value = false
  await fetchHoldingData()
}

async function onOperationRemove(row: OperationData) {
  await apiOperationRemove({
    id: row.id
  })
  await fetchHoldingData()
}

async function onRemove(row: HoldingOperationData) {
  await apiFlag({
    id: row.holding.id,
    flag: HOLDING_FLAG_REMOVED
  })
  await fetchHoldingData()
}

function getHoldingKey(row: HoldingOperationData): string {
  // console.log(row.holding.id)
  return row.holding.id.toString()
}

function onExpandChanged(rows: HoldingOperationData, expandedRows: HoldingOperationData[]) {
  expandRows.value = expandedRows.map((x) => x.holding.id.toString())
}
</script>

<template>
  <ContentWrap title="持仓">
    <ElRow :gutter="24">
      <ElButton class="my-4" type="primary" @click="createDialogVisible=true">增加</ElButton>
    </ElRow>
    <ElRow :gutter="24">
      <ElTable :data="data" :row-key="getHoldingKey" :expand-row-keys="expandRows" @expand-change="onExpandChanged" stripe :border="true">
        <ElTableColumn type="index" width="40" />
        <ElTableColumn type="expand">
          <template #default="{ row }">
            <div class="mx-24px my-8px">
              <ElRow :gutter="24">
                <ElCol :span="12">
                  <h4>操作记录({{ row.items.length }})</h4>
                </ElCol>
                <ElCol :span="12">
                  <ElButton type="primary" style="float: right;" @click="onOperation(row)">增加操作</ElButton>
                </ElCol>
              </ElRow>
            </div>
            <div class="mx-24px my-8px">       
              <ElTable size="small" :data="row.items" stripe :border="true">
                <ElTableColumn type="index" width="40" />
                <ElTableColumn label="操作" prop="action" width="60">
                  <template #default="{ row }">
                    {{ row.action == OPERATION_ACTION_BUY ? '买入' : '卖出' }}
                  </template>
                </ElTableColumn>
                <ElTableColumn label="数量" prop="quantity" min-width="80" />
                <ElTableColumn label="价格" prop="price" min-width="80" />
                <ElTableColumn label="费用" prop="expense" min-width="80" />
                <ElTableColumn label="创建时间" prop="created" min-width="120">
                  <template #default="{ row }">
                    {{ formatToDateTime(row.created) }}
                  </template>
                </ElTableColumn>
                <ElTableColumn label="备注" prop="comment" />
                <ElTableColumn label="" min-width="160">
                  <template #default="{ row }">
                    <ElButton size="small" @click="onOperationRemove(row)">删除</ElButton>
                  </template>
                </ElTableColumn>
              </ElTable>
            </div>
          </template>
        </ElTableColumn>
        <!-- <ElTableColumn prop="id" label="ID" width="50"></ElTableColumn> -->
          <!-- <ElTableColumn prop="type" label="Type" width="50"></ElTableColumn> -->
          <ElTableColumn prop="holding.code" label="代码" min-width="80"></ElTableColumn>
          <ElTableColumn prop="holding.name" label="名称" min-width="80"></ElTableColumn>
          <!-- <ElTableColumn prop="flag" label="Flag" width="50"></ElTableColumn> -->
          <ElTableColumn prop="holding.quantity" label="数量" min-width="60"></ElTableColumn>
          <ElTableColumn prop="holding.expense" label="成本" min-width="60"></ElTableColumn>
          <ElTableColumn prop="holding.price_avg" label="均价" min-width="80"></ElTableColumn>
          <ElTableColumn prop="holding.price_cur" label="现价" min-width="80"></ElTableColumn>
          <ElTableColumn prop="holding.revenue" label="收益" min-width="80"></ElTableColumn>
          <ElTableColumn prop="holding.profit" label="利润" min-width="80"></ElTableColumn>
          <ElTableColumn prop="holding.profit_percent" label="利润率 %" min-width="100"></ElTableColumn>
          <ElTableColumn prop="holding.created" label="创建时间" min-width="120">
            <template #default="{ row }">
              {{ formatToDate(row.holding.created) }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="holding.updated" label="更新时间" min-width="120">
            <template #default="{ row }">
              {{ formatToDate(row.holding.updated) }}
            </template>
          </ElTableColumn>
          <ElTableColumn label="" width="160">
            <template #default="{ row }">
              <ElButton size="small" @click="onRemove(row)">删除</ElButton>
            </template>
          </ElTableColumn>      
      </ElTable>
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
    <ElDialog v-model="operationDialogVisible" :destroy-on-close="true" width="25%">
      <template #header>
        <ElText tag="b">新增操作记录</ElText>
      </template>
      <template #default>
        <ElForm :model="operationForm" label-position="right" label-width="auto">
          <ElFormItem label="代码">
            <ElInput v-model="operationForm.code" :disabled="true" />
          </ElFormItem>
          <ElFormItem label="名称">
            <ElInput v-model="operationForm.name" :disabled="true" />
          </ElFormItem>
          <ElFormItem label="操作">
            <ElRadioGroup v-model="operationForm.action">
              <ElRadioButton :value="OPERATION_ACTION_BUY">买入</ElRadioButton>
              <ElRadioButton :value="OPERATION_ACTION_SELL">卖出</ElRadioButton>
            </ElRadioGroup>
          </ElFormItem>
          <ElFormItem label="数量" @change="onQuantityBlur">
            <ElInput v-model="operationForm.quantity" />
          </ElFormItem>
          <ElFormItem label="价格" @change="onPriceBlur">
            <ElInput v-model="operationForm.price" />
          </ElFormItem>
          <ElFormItem label="费用">
            <ElInput v-model="operationForm.expense" />
          </ElFormItem>
          <ElFormItem label="备注">
            <ElInput v-model="operationForm.comment" />
          </ElFormItem>
        </ElForm>
      </template>
      <template #footer>
        <ElButton @click="operationDialogVisible=false">取消</ElButton>
        <ElButton type="primary" @click="onAddOperation">确定</ElButton>
      </template>        
    </ElDialog>
  </ContentWrap>
</template>