<script lang="ts">

interface HoldingOperationItem {
  holding: HoldingItem
  items: OperationItem[]
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
  date: Date
  quantity: number
  price: number
  expense: number
  comment?: string    
}

</script>

<script setup lang="ts">
import { apiCreate, apiFlag, apiOperationCreate, apiOperationList, apiOperationRemove } from '@/api/holding'
import { HOLDING_FLAG_REMOVED, OPERATION_ACTION_BUY, OPERATION_ACTION_SELL } from '@/api/holding/types'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref } from 'vue'
import {
  ElText, ElDialog, ElButton, ElRow, ElCol, ElInput, ElForm, ElFormItem, ElTable, ElTableColumn,
  ElRadioGroup, ElRadioButton, ElDatePicker
 } from 'element-plus'
import { formatToDate, formatToDateTime } from '@/utils/dateUtil'
import { TYPE_INDEX, TYPE_STOCK } from '@/api/data/types'
import { useRouter } from 'vue-router'
import { getHoldingData, HoldingItem, OperationItem } from '@/calc/holding'

const { push } = useRouter()

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
  date: new Date(),
  quantity: 0,
  price: 0,
  expense: 0,
  comment: ''
})
const data = ref<HoldingOperationItem[]>([])
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
    holding!.items.unshift(item)
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

function onOperation(row: HoldingOperationItem) {
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
    comment: operationForm.value.comment,
    created: operationForm.value.date
  })
  operationDialogVisible.value = false
  await fetchHoldingData()
}

async function onOperationRemove(row: OperationItem) {
  await apiOperationRemove({
    id: row.id
  })
  await fetchHoldingData()
}

async function onRemove(row: HoldingOperationItem) {
  await apiFlag({
    id: row.holding.id,
    flag: HOLDING_FLAG_REMOVED
  })
  await fetchHoldingData()
}

async function onDetail(row: HoldingOperationItem) {
  push({
    path: '/holding/detail',
    query: {
      id: row.holding.id
    }
  })
}

function getHoldingKey(row: HoldingOperationItem): string {
  // console.log(row.holding.id)
  return row.holding.id.toString()
}

function onExpandChanged(rows: HoldingOperationItem, expandedRows: HoldingOperationItem[]) {
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
        <!-- <ElTableColumn prop="id" label="ID" width="50" /> -->
          <!-- <ElTableColumn prop="type" label="Type" width="50" /> -->
          <ElTableColumn prop="holding.code" label="代码" min-width="80" />
          <ElTableColumn prop="holding.name" label="名称" min-width="80" />
          <!-- <ElTableColumn prop="flag" label="Flag" width="50" /> -->
          <ElTableColumn prop="holding.quantity" label="数量" min-width="60" />
          <ElTableColumn prop="holding.expense" label="成本" min-width="60" />
          <ElTableColumn prop="holding.price_avg" label="均价" min-width="80" />
          <ElTableColumn prop="holding.price_cur" label="现价" min-width="80">
            <template #default="{ row }">
              {{ `${row.holding.price_cur}[${row.holding.price_date.substring(5)}]` }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="holding.revenue" label="收益" min-width="80" />
          <ElTableColumn prop="holding.profit" label="利润" min-width="80" />
          <ElTableColumn prop="holding.profit_rate" label="利润率 %" min-width="100" />
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
              <ElButton size="small" @click="onDetail(row)">详情</ElButton>
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
            <ElRow :gutter="24">
              <ElCol :span="10">
                <ElRadioGroup v-model="operationForm.action">
                  <ElRadioButton :value="OPERATION_ACTION_BUY">买入</ElRadioButton>
                  <ElRadioButton :value="OPERATION_ACTION_SELL">卖出</ElRadioButton>
                </ElRadioGroup>
              </ElCol>
              <ElCol :span="14">
                <ElDatePicker
                  v-model="operationForm.date"
                  type="date"
                  placeholder="选择日期"
                  style="width: 100%"
                />
              </ElCol>
            </ElRow>
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