<script lang="ts">

interface FundsForm {
  amount?: number
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
  expense: number | string
  comment?: string    
}

</script>

<script setup lang="ts">
import { apiCreate, apiFlag, apiOperationCreate, apiOperationRemove } from '@/api/holding'
import { HOLDING_FLAG_REMOVED, HoldingRecordItem, OPERATION_ACTION_BUY, OPERATION_ACTION_SELL } from '@/api/holding/types'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref } from 'vue'
import {
  ElText, ElDialog, ElButton, ElRow, ElCol, ElInput, ElForm, ElFormItem, ElTable, ElTableColumn, ElTooltip,
  ElRadioGroup, ElRadioButton, ElDatePicker, ElMessageBox, ElDescriptions, ElDescriptionsItem, ElDivider
 } from 'element-plus'
import { formatToDate, formatToDateTime } from '@/utils/dateUtil'
import { TYPE_INDEX, TYPE_STOCK } from '@/api/data/types'
import { useRouter } from 'vue-router'
import { calcFundsData, FUNDS_STOCK, FundsData } from '@/calc/funds'
import { getHoldListData, HoldingListItem } from '@/calc/holding'
import { apiGetFunds, apiUpdateFunds } from '@/api/funds'
import { KLineDialog } from '@/components/KLine'

const { push } = useRouter()

const fundsDialogVisible = ref<boolean>(false)
const createDialogVisible = ref<boolean>(false)
const operationDialogVisible = ref<boolean>(false)
const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<any>({})

const fundsForm = ref<FundsForm>({
  amount: undefined
})

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
const data = ref<HoldingListItem[]>([]) // ref<HoldingInfoItem[]>([])
// const total = ref<ProfitTotalData>()
const funds = ref<FundsData>()
const expandRows = ref<string[]>([])

async function fetchHoldingData() {
  const fret = await apiGetFunds({})
  if (fret.result) {
    data.value = await getHoldListData()
    funds.value = calcFundsData(fret.result, data.value)
    data.value = data.value.reverse()
    data.value.forEach((v) => {
      v.items = v.items.reverse()
   })    
  } else
    funds.value = undefined
}

onMounted(async () => {
  await fetchHoldingData()
})

async function onFunds() {
  if (fundsForm.value.amount) {
    await apiUpdateFunds({
      type: FUNDS_STOCK,
      amount: fundsForm.value.amount
    })
    fundsDialogVisible.value = false
    await fetchHoldingData()    
  }
}

async function onAdd() {
  const ret = await apiCreate({
    type: createForm.value.type == '股票' ? TYPE_STOCK : TYPE_INDEX,
    code: createForm.value.code
  })
  createDialogVisible.value = false
  await fetchHoldingData()
}

function onOperation(row: HoldingRecordItem) {
  operationForm.value.holding = row.id
  operationForm.value.type = row.type
  operationForm.value.code = row.code
  operationForm.value.name = row.name
  operationDialogVisible.value = true
}

function onPriceBlur() {
  operationForm.value.expense = (operationForm.value.quantity * operationForm.value.price).toFixed(2)
}

function onQuantityBlur() {
  operationForm.value.expense = (operationForm.value.quantity * operationForm.value.price).toFixed(2)
}

async function onAddOperation() {
  const ret = await apiOperationCreate({
    holding: operationForm.value.holding,
    action: operationForm.value.action,
    quantity: operationForm.value.quantity,
    price: operationForm.value.price,
    expense: (typeof operationForm.value.expense === 'string' ? parseFloat(operationForm.value.expense) : operationForm.value.expense),
    comment: operationForm.value.comment,
    created: operationForm.value.date
  })
  operationDialogVisible.value = false
  await fetchHoldingData()
}

async function onOperationRemove(id: number) {
  const confirm = await ElMessageBox.confirm(
    '是否确认删除?',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
  if (confirm) {
    await apiOperationRemove({
      id: id
    })
    await fetchHoldingData()
  }
}

async function onRemove(id: number) {
  const confirm = await ElMessageBox.confirm(
    '是否确认删除?',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
  if (confirm) {
    await apiFlag({
      id: id,
      flag: HOLDING_FLAG_REMOVED
    })
    await fetchHoldingData()
  }
}

async function onDetail(id: number) {
  const ids = data.value.map((x) => x.record.id)
  console.log('onDetail', id, ids)
  push({
    path: '/holding/detail',
    query: {
      id: id,
      ids: data.value.map((x) => x.record.id).join(',')
    }
  })
}

function getHoldingKey(row: HoldingListItem): string {
  return row.record.id.toString() // row.holding.id.toString()
}

function onExpandChanged(rows: HoldingListItem, expandedRows: HoldingListItem[]) {
  expandRows.value = expandedRows.map((x) => x.record.id.toString())
}

function onRecordClick(row: HoldingRecordItem) {
  reqParam.value = {
    code: row.code,
    name: row.name,
    type: row.type,
  //   start: row.record.created,
  //   end: new Date()
  }
  klineDialogVisible.value = true
}
</script>

<template>
  <ContentWrap>
    <ElDescriptions :column="3" title="资金信息" :border="true" label-width="6%">
      <ElDescriptionsItem label="总资产" :span="3">
        <ElTooltip effect="dark" content="可用 + 市值" placement="top">
          <ElText tag="b">{{ funds?.total.toFixed(2) }}</ElText>
        </ElTooltip>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="可用">
        <ElText tag="b">{{ funds?.available.toFixed(2) }} / </ElText>
        <ElTooltip effect="dark" content="可用/本金%" placement="top">
          <ElText tag="b">{{ ((funds?.available / funds?.amount) * 100).toFixed(2) }}%</ElText>
        </ElTooltip>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="成本">
        <ElText tag="b">{{ -funds?.expense.toFixed(2) }} / </ElText>
        <ElTooltip effect="dark" content="成本/本金%" placement="top">
          <ElText tag="b">{{ -((funds?.expense / funds?.amount) * 100).toFixed(2) }}%</ElText>
        </ElTooltip>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="本金">
        <template #default>
          <ElText tag="b">{{ funds?.amount.toFixed(2) }}</ElText>
          <ElButton size="small" style="float: right" @click="fundsDialogVisible = true">调整</ElButton>
        </template>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="市值"><ElText tag="b">{{ funds?.revenue.toFixed(2) }}</ElText></ElDescriptionsItem>
      <ElDescriptionsItem label="盈亏"><ElText tag="b">{{ funds?.profit.toFixed(2) }}</ElText></ElDescriptionsItem>
      <ElDescriptionsItem label="盈亏率"><ElText tag="b">{{ funds?.profit_rate ? ((funds.profit_rate) * 100).toFixed(2) + '%' : '-' }}</ElText></ElDescriptionsItem>
    </ElDescriptions>
    <ElDivider calss="mx-8px" content-position="left">持股记录</ElDivider>
    <ElRow :gutter="24">
      <ElButton class="my-4" type="primary" @click="createDialogVisible=true">增加持股</ElButton>
    </ElRow>
    <ElRow :gutter="24">
      <ElTable :data="data" :row-key="getHoldingKey" :expand-row-keys="expandRows" @expand-change="onExpandChanged" stripe :border="true">
        <ElTableColumn type="index" width="40" />
        <ElTableColumn type="expand">
          <template #default="{ row }">
            <div class="mx-24px my-8px">
              <ElRow :gutter="24">
                  <ElText tag="b">操作记录 ({{ row.items.length }})</ElText>
                  <ElButton size="small" class="mx-8" type="primary" @click="onOperation(row.record)">增加操作</ElButton>
              </ElRow>
            </div>
            <div class="mx-24px my-8px">       
              <ElTable size="small" :data="row.items" stripe :border="true">
                <ElTableColumn type="index" width="40" />
                <ElTableColumn label="操作" prop="action" width="80">
                  <template #default="{ row }">
                    {{ row.action == OPERATION_ACTION_BUY ? '买入' : '卖出' }}
                  </template>
                </ElTableColumn>
                <ElTableColumn label="数量" prop="quantity" min-width="80" />
                <ElTableColumn label="买入" prop="price" min-width="80">
                  <template #default="{ row }">
                    {{ row.price.toFixed(2) }}
                  </template>
                </ElTableColumn>
                <ElTableColumn label="费用" prop="expense" min-width="80">
                  <template #default="{ row }">
                    {{ row.expense.toFixed(2) }}
                  </template>
                </ElTableColumn>
                <ElTableColumn label="操作时间" prop="created" min-width="120">
                  <template #default="{ row }">
                    {{ formatToDateTime(row.created) }}
                  </template>
                </ElTableColumn>
                <ElTableColumn label="备注" prop="comment" />
                <ElTableColumn label="" min-width="160">
                  <template #default="{ row }">
                    <ElButton size="small" @click="onOperationRemove(row.id)">删除</ElButton>
                  </template>
                </ElTableColumn>
              </ElTable>
            </div>
          </template>
        </ElTableColumn>
        <!-- <ElTableColumn prop="id" label="ID" width="50" /> -->
          <!-- <ElTableColumn prop="type" label="Type" width="50" /> -->
          <ElTableColumn prop="record.code" label="名称/代码" min-width="60">
            <template #header>
              <ElText>名称/代码</ElText>
            </template>
            <template #default="{ row }">
              <div @click="onRecordClick(row.record)">
                <div><ElText tag="b">{{ row.record.name }}</ElText></div>
                <div><ElText tag="b">{{ row.record.code }}</ElText></div>
              </div>
            </template>
          </ElTableColumn>
          <!-- <ElTableColumn prop="record.name" label="名称" min-width="80">
            <template #header>
              <ElText>名称</ElText>
            </template>
          </ElTableColumn> -->
          <ElTableColumn prop="record.quantity" label="持仓/占比" min-width="100">
            <template #header>
              <ElTooltip effect="dark" content="持仓/仓位%" placement="top">
                <ElText>持仓/占比</ElText>
              </ElTooltip>
            </template>
            <template #default="{ row }">
              {{ `${row.record.quantity} / ${((row.record.quantity / funds?.holding) * 100).toFixed(2)}%` }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="record.expense" label="成本/占比" min-width="120">
            <template #header>
              <ElTooltip effect="dark" content="成本/费用%" placement="top">
                <ElText>成本/占比</ElText>
              </ElTooltip>
            </template>
            <template #default="{ row }">
            {{ `${-row.record.expense} / ${((row.record.expense / funds?.expense) * 100).toFixed(2)}%` }}
            </template>
          </ElTableColumn>
          <ElTableColumn label="均价" min-width="60">
            <template #header>
              <ElTooltip effect="dark" content="成本/持仓" placement="top">
                <ElText>均价</ElText>
              </ElTooltip>
            </template>
            <template #default="{ row }">
              {{ `${row.calc.price_avg? row.calc.price_avg.toFixed(2) : '-'}` }}
            </template>
          </ElTableColumn>
          <ElTableColumn label="现价/日期" min-width="100">
            <template #header>
              <ElTooltip effect="dark" content="当日价格" placement="top">
                <ElText>现价/日期</ElText>
              </ElTooltip>
            </template>
            <template #default="{ row }">
              {{ `${row.calc.price_cur?.toFixed(2)} / ${row.calc.date_cur?.substring(5)}` }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="calc.revenue" label="市值/占比" min-width="120">
            <template #header>
              <ElTooltip effect="dark" content="市值/总市值%" placement="top">
                <ElText>市值/占比</ElText>
              </ElTooltip>
            </template>
            <template #default="{ row }">
              {{ `${row.calc.revenue?.toFixed(2)} / ${((row.calc.revenue / funds?.revenue) * 100).toFixed(2)}%` }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="calc.profit" label="盈亏/占比" min-width="120">
            <template #header>
              <ElTooltip effect="dark" content="盈亏/总盈亏%" placement="top">
                <ElText>盈亏/占比</ElText>
              </ElTooltip>
            </template>
            <template #default="{ row }">
              <div :class="row.calc.profit > 0 ? 'red-text' : (row.calc.profit < 0 ? 'green-text' : '')">
                {{ `${row.calc.profit?.toFixed(2)} /  ${((row.calc.profit / funds?.profit) * 100).toFixed(2)}%` }}
              </div>
            </template>
          </ElTableColumn>
          <ElTableColumn label="盈亏率 %" min-width="80">
            <template #header>
              <ElTooltip effect="dark" content="盈亏/成本%" placement="top">
                <ElText>盈亏率%</ElText>
              </ElTooltip>
            </template>
            <template #default="{ row }">
              <div :class="row.calc.profit_rate > 0 ? 'red-text' : (row.calc.profit_rate < 0 ? 'green-text' : '')">
                {{ `${row.calc.profit_rate? (row.calc.profit_rate * 100).toFixed(2) + '%' : '-'}` }}
              </div>
            </template>
          </ElTableColumn>
          <ElTableColumn prop="record.created" label="创建时间" min-width="120">
            <template #header>
              <ElText>创建时间</ElText>
            </template>
            <template #default="{ row }">
              {{ formatToDate(row.record.created) }}
            </template>
          </ElTableColumn>
          <!-- <ElTableColumn label="更新时间" min-width="120">
            <template #default="{ row }">
              {{ formatToDate(row.record.updated) }}
            </template>
          </ElTableColumn> -->
          <ElTableColumn label="" width="160">
            <template #default="{ row }">
              <ElButton size="small" @click="onDetail(row.record.id)">详情</ElButton>
              <ElButton size="small" @click="onRemove(row.record.id)">删除</ElButton>
            </template>
          </ElTableColumn>      
      </ElTable>
    </ElRow>
    <ElDialog v-model="fundsDialogVisible" :destroy-on-close="true" width="25%">
      <template #header>
        <ElText tag="b">资金数据</ElText>
      </template>
      <template #default>
        <ElForm :model="fundsForm" label-position="right" label-width="auto">
          <ElFormItem label="资金调整">
            <ElInput v-model="fundsForm.amount" placeholder="增加资金为正，提取资金为负..">
              <template #append>元</template>
            </ElInput>
          </ElFormItem>
        </ElForm>
      </template>
      <template #footer>
        <ElButton @click="fundsDialogVisible=false">取消</ElButton>
        <ElButton type="primary" @click="onFunds">确定</ElButton>
      </template>         
    </ElDialog>
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
            <ElInput v-model="operationForm.price">
              <template #append>元</template>
            </ElInput>
          </ElFormItem>
          <ElFormItem label="费用">
            <ElInput v-model="operationForm.expense">
              <template #append>元</template>
            </ElInput>
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
    <KLineDialog :visible="klineDialogVisible" :req-param="reqParam" @update:on-close="klineDialogVisible = false" width="60%" />
  </ContentWrap>
</template>
<style lang="css" scoped>
.green-text {
    color: green;
}

.red-text {
    color: red;
}
</style>