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
import {
  apiCreate,
  apiFlag,
  apiOperationCreate,
  apiOperationList,
  apiOperationRemove,
  apiRecord
} from '@/api/holding'
import {
  HOLDING_FLAG_ACTIVE,
  HOLDING_FLAG_REMOVED,
  HOLDING_FLAG_SOLDOUT,
  HoldingRecordItem,
  OPERATION_ACTION_BUY,
  OPERATION_ACTION_SELL,
  OPERATION_ACTION_SOLDOUT,
  OPERATION_ACTION_INTEREST
} from '@/api/holding/types'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref, watch } from 'vue'
import {
  ElText,
  ElDialog,
  ElButton,
  ElRow,
  ElCol,
  ElInput,
  ElForm,
  ElFormItem,
  ElTable,
  ElTableColumn,
  ElTooltip,
  ElRadioGroup,
  ElRadioButton,
  ElDatePicker,
  ElMessageBox,
  ElDescriptions,
  ElDescriptionsItem,
  ElDivider,
  ElCheckbox
} from 'element-plus'
import { formatToDateTime } from '@/utils/dateUtil'
import { TYPE_INDEX, TYPE_STOCK } from '@/api/data/types'
import { useRouter } from 'vue-router'
import { calcFundsData, FUNDS_STOCK, FundsData } from '@/calc/funds'
import { calcHoldingData, calcSoldoutData, HoldingListItem, SoldoutListItem } from '@/calc/holding'
import { apiGetFunds, apiUpdateFunds } from '@/api/funds'
import { formatNumberString, formatRateString, formatRateString2 } from '@/utils/fmtUtil'
import { KLineDialog } from '@/components/KLine'

const { push } = useRouter()

const fundsDialogVisible = ref<boolean>(false)
const createDialogVisible = ref<boolean>(false)
const operationDialogVisible = ref<boolean>(false)
const klineDialogVisible = ref<boolean>(false)
const useLocale = ref<boolean>(false)
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
const soldoutData = ref<SoldoutListItem[]>([])
const soldoutExpandRows = ref<string[]>([])
const showSoldoutTable = ref<boolean>(true)

async function fetchData() {
  const holdingData = await apiRecord({ flag: HOLDING_FLAG_ACTIVE })
  data.value = holdingData.result.map((item: HoldingRecordItem) => ({
    record: item,
    calc: undefined,
    items: []
  }))
  data.value = data.value.reverse()
  for (const holding of data.value) {
    holding.calc = await calcHoldingData(holding.record, useLocale.value)
    holding.items = (
      await apiOperationList({
        holding: holding.record.id
      })
    ).result
  }

  const soldoutHoldingData = await apiRecord({ flag: HOLDING_FLAG_SOLDOUT })
  soldoutData.value = soldoutHoldingData.result.map((item: HoldingRecordItem) => ({
    record: item,
    calc: undefined,
    items: []
  }))
  soldoutData.value = soldoutData.value.reverse()
  for (const holding of soldoutData.value) {
    holding.items = (
      await apiOperationList({
        holding: holding.record.id
      })
    ).result
    holding.calc = calcSoldoutData(holding.items)
  }

  const fret = await apiGetFunds({})
  if (fret.result) {
    funds.value = calcFundsData(fret.result, data.value, soldoutData.value)
  } else {
    funds.value = undefined
  }
}

async function fetchHoldingData() {
  await fetchData()
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

const operationHoldingQuantity = ref<number>(0)

function onOperation(row: HoldingRecordItem) {
  operationHoldingQuantity.value = row.quantity
  operationForm.value.holding = row.id
  operationForm.value.type = row.type
  operationForm.value.code = row.code
  operationForm.value.name = row.name
  operationDialogVisible.value = true
}

function onPriceBlur() {
  operationForm.value.expense = (operationForm.value.quantity * operationForm.value.price).toFixed(
    2
  )
}

function onQuantityBlur() {
  operationForm.value.expense = (operationForm.value.quantity * operationForm.value.price).toFixed(
    2
  )
}

watch(
  () => operationForm.value.action,
  (newVal) => {
    if (newVal === OPERATION_ACTION_INTEREST) {
      operationForm.value.quantity = 0
      operationForm.value.price = 0
    }
  }
)

watch(
  () => operationForm.value.action,
  (newVal) => {
    if (newVal === OPERATION_ACTION_INTEREST) {
      operationForm.value.quantity = 0
      operationForm.value.price = 0
    }
  }
)

async function onAddOperation() {
  if (
    operationForm.value.action === OPERATION_ACTION_SELL &&
    operationForm.value.quantity > operationHoldingQuantity.value
  ) {
    await ElMessageBox.alert('卖出数量不能大于持仓数量', '错误', {
      confirmButtonText: '确定',
      type: 'error'
    })
    return
  }

  const ret = await apiOperationCreate({
    holding: operationForm.value.holding,
    action: operationForm.value.action,
    quantity: operationForm.value.quantity,
    price: operationForm.value.price,
    expense:
      typeof operationForm.value.expense === 'string'
        ? parseFloat(operationForm.value.expense)
        : operationForm.value.expense,
    comment: operationForm.value.comment,
    created: operationForm.value.date
  })

  operationDialogVisible.value = false
  await fetchHoldingData()
}

async function onOperationRemove(id: number) {
  const confirm = await ElMessageBox.confirm('是否确认删除?', '提示', {
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
  const confirm = await ElMessageBox.confirm('是否确认删除?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
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
  // console.log('onDetail', id, ids)
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

function onSoldoutExpandChanged(rows: HoldingListItem, expandedRows: HoldingListItem[]) {
  soldoutExpandRows.value = expandedRows.map((x) => x.record.id.toString())
}

function onRecordClick(row: HoldingRecordItem) {
  reqParam.value = {
    code: row.code,
    name: row.name,
    type: row.type
    //   start: row.record.created,
    //   end: new Date()
  }
  klineDialogVisible.value = true
}

function onReload() {
  fetchHoldingData()
}
</script>

<template>
  <ContentWrap>
    <ElDescriptions :column="3" title="资金信息" :border="true" label-width="6%">
      <ElDescriptionsItem label="总资产" :span="3">
        <ElTooltip effect="dark" content="可用 + 市值" placement="top">
          <ElText tag="b">{{ formatNumberString(funds?.total) }}</ElText>
        </ElTooltip>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="可用">
        <ElText tag="b">{{ formatNumberString(funds?.available) }} / </ElText>
        <ElTooltip effect="dark" content="可用/本金%" placement="top">
          <ElText tag="b">{{ formatRateString2(funds?.available, funds?.amount) }}</ElText>
        </ElTooltip>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="成本">
        <ElText tag="b"
          >{{ formatNumberString(funds?.expense ? -funds?.expense : undefined) }} /
        </ElText>
        <ElTooltip effect="dark" content="成本/本金%" placement="top">
          <ElText tag="b">{{
            formatRateString2(funds?.expense ? -funds?.expense : undefined, funds?.amount)
          }}</ElText>
        </ElTooltip>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="本金">
        <template #default>
          <ElText tag="b">{{ funds?.amount.toFixed(2) }}</ElText>
          <ElButton size="small" style="float: right" @click="fundsDialogVisible = true"
            >调整</ElButton
          >
        </template>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="市值"
        ><ElText tag="b">{{ formatNumberString(funds?.revenue) }}</ElText></ElDescriptionsItem
      >
      <ElDescriptionsItem label="盈亏">
        <ElTooltip effect="dark" content="清仓盈亏合计" placement="top">
          <ElText tag="b">
            {{ formatNumberString(funds?.profit) }}
            <template v-if="funds?.soldout_profit !== 0 && showSoldoutTable">
              (+ {{ formatNumberString(funds?.soldout_profit) }} =
              {{ formatNumberString((funds?.profit || 0) + (funds?.soldout_profit || 0)) }})
            </template>
          </ElText>
        </ElTooltip>
      </ElDescriptionsItem>
      <ElDescriptionsItem label="盈亏率">
        <ElTooltip effect="dark" content="清仓盈亏率合计" placement="top">
          <ElText tag="b">{{
            formatRateString(funds?.profit_rate)
          }} <template v-if="funds?.soldout_profit !== 0 && showSoldoutTable">({{
            formatRateString(
              funds?.expense === 0
                ? 0
                : ((funds?.profit || 0) + (funds?.soldout_profit || 0)) / -funds?.expense
            )
          }})</template></ElText>
        </ElTooltip>
      </ElDescriptionsItem>
    </ElDescriptions>
    <ElDivider class="mx-8px" content-position="left"><span style="font-weight: bold;">持股记录</span></ElDivider>
    <ElRow :gutter="24">
      <ElCol :span="12">
        <ElButton class="my-4" type="primary" @click="createDialogVisible = true"
          >增加持股</ElButton
        >
      </ElCol>
      <ElCol :span="12">
        <ElButton class="my-4" style="float: right" @click="onReload">刷新记录</ElButton>
        <ElCheckbox
          v-model="useLocale"
          class="my-4"
          style="float: right; margin-right: 12px"
          label="使用本地数据"
        />
      </ElCol>
    </ElRow>
    <ElRow :gutter="24">
      <ElTable
        :data="data"
        :row-key="getHoldingKey"
        :expand-row-keys="expandRows"
        @expand-change="onExpandChanged"
        stripe
        :border="true"
        :default-sort="{ prop: 'record.created', order: 'descending' }"
      >
        <ElTableColumn type="index" width="40" />
        <ElTableColumn type="expand">
          <template #default="{ row }">
            <div class="mx-24px my-8px">
              <ElRow :gutter="24">
                <ElText tag="b">操作记录 ({{ row.items.length }})</ElText>
                <ElButton size="small" class="mx-8" type="primary" @click="onOperation(row.record)"
                  >增加操作</ElButton
                >
              </ElRow>
            </div>
            <div class="mx-24px my-8px">
              <ElTable
                size="small"
                :data="row.items"
                stripe
                :border="true"
                :default-sort="{ prop: 'created', order: 'descending' }"
              >
                <ElTableColumn type="index" width="40" />
                <ElTableColumn label="操作" prop="action" width="80">
                  <template #default="{ row }">
                    <ElText
                      :class="
                        row.action == OPERATION_ACTION_BUY
                          ? 'red-text'
                          : row.action == OPERATION_ACTION_SELL
                            ? 'green-text'
                            : ''
                      "
                    >
                      {{
                        row.action == OPERATION_ACTION_BUY
                          ? '买入'
                          : row.action == OPERATION_ACTION_SELL
                            ? '卖出'
                            : row.action == OPERATION_ACTION_SOLDOUT
                              ? '清仓'
                              : '计息'
                      }}
                    </ElText>
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
        <ElTableColumn prop="record.code" label="名称/代码" min-width="80">
          <template #header>
            <ElText>名称/代码</ElText>
          </template>
          <template #default="{ row }">
            <div @click="onRecordClick(row.record)">
              <div
                ><ElText tag="b">{{ row.record.name }}</ElText></div
              >
              <div
                ><ElText tag="b">{{ row.record.code }}</ElText></div
              >
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
            {{ formatNumberString(row.record.quantity) }} /
            {{ formatRateString2(row.record.quantity, funds?.holding) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="record.expense" label="成本/占比" min-width="110">
          <template #header>
            <ElTooltip effect="dark" content="成本/费用%" placement="top">
              <ElText>成本/占比</ElText>
            </ElTooltip>
          </template>
          <template #default="{ row }">
            {{ formatNumberString(row.record.expense) }} /
            {{ formatRateString2(row.record.expense, funds?.expense) }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="均价/价差" min-width="80">
          <template #header>
            <ElTooltip effect="dark" content="（成本/持仓）/(现价-均价)" placement="top">
              <ElText>均价/价差</ElText>
            </ElTooltip>
          </template>
          <template #default="{ row }">
            {{ formatNumberString(row.calc?.price_avg) }} /
            <ElText
              :class="
                row.calc?.price_cur - row.calc?.price_avg > 0
                  ? 'red-text'
                  : row.calc?.price_cur - row.calc?.price_avg < 0
                    ? 'green-text'
                    : 'red-text'
              "
            >
              {{ formatNumberString(row.calc?.price_cur - row.calc?.price_avg) }}
            </ElText>
          </template>
        </ElTableColumn>
        <ElTableColumn label="现价/日期" min-width="100">
          <template #header>
            <ElTooltip effect="dark" content="当日价格" placement="top">
              <ElText>现价/日期</ElText>
            </ElTooltip>
          </template>
          <template #default="{ row }">
            {{ formatNumberString(row.calc?.price_cur) }} [{{
              `${row.calc ? row.calc?.date_cur?.substring(5) : '-'}`
            }}]
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc.profit" label="昨差/昨差率%" min-width="100">
          <template #header>
            <ElTooltip effect="dark" content="与前一日价格差/价格差率%" placement="top">
              <ElText>昨差/昨差率%</ElText>
            </ElTooltip>
          </template>
          <template #default="{ row }">
            <div
              :class="
                row.calc?.pre_price_rate > 0
                  ? 'red-text'
                  : row.calc?.pre_price_rate < 0
                    ? 'green-text'
                    : ''
              "
            >
              {{ formatNumberString(row.calc?.price_cur - row.calc?.pre_price) }} /
              {{ formatRateString(row.calc?.pre_price_rate) }}
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc.revenue" label="市值/占比" min-width="120">
          <template #header>
            <ElTooltip effect="dark" content="市值/总市值%" placement="top">
              <ElText>市值/占比</ElText>
            </ElTooltip>
          </template>
          <template #default="{ row }">
            {{ formatNumberString(row.calc?.revenue) }} /
            {{ formatRateString2(row.calc?.revenue, funds?.revenue) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc.profit" label="盈亏/占比" min-width="120">
          <template #header>
            <ElTooltip effect="dark" content="盈亏/总盈亏%" placement="top">
              <ElText>盈亏/占比</ElText>
            </ElTooltip>
          </template>
          <template #default="{ row }">
            <div
              :class="row.calc?.profit > 0 ? 'red-text' : row.calc?.profit < 0 ? 'green-text' : ''"
            >
              {{ formatNumberString(row.calc?.profit) }} /
              {{ formatRateString2(Math.abs(row.calc?.profit), funds?.profit ? Math.abs(funds?.profit) : undefined) }}
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn label="盈亏率 %" min-width="60">
          <template #header>
            <ElTooltip effect="dark" content="盈亏/成本%" placement="top">
              <ElText>盈亏率%</ElText>
            </ElTooltip>
          </template>
          <template #default="{ row }">
            <div
              :class="
                row.calc?.profit_rate > 0
                  ? 'red-text'
                  : row.calc?.profit_rate < 0
                    ? 'green-text'
                    : ''
              "
            >
              {{ formatRateString(row.calc?.profit_rate) }}
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc.profit" label="昨差/昨差率%" min-width="100">
          <template #header>
            <ElTooltip effect="dark" content="与前一日盈利差/盈利差率%" placement="top">
              <ElText>昨差/昨差率%</ElText>
            </ElTooltip>
          </template>
          <template #default="{ row }">
            <div
              :class="
                row.calc?.pre_profit_rate > 0
                  ? 'red-text'
                  : row.calc?.pre_profit_rate < 0
                    ? 'green-text'
                    : ''
              "
            >
              {{ formatNumberString(row.calc?.pre_profit_diff) }} /
              {{ formatRateString(row.calc?.pre_profit_rate) }}
            </div>
          </template>
        </ElTableColumn>
        <!-- <ElTableColumn prop="record.created" label="创建时间" min-width="120">
            <template #header>
              <ElText>创建时间</ElText>
            </template>
            <template #default="{ row }">
              {{ formatToDate(row.record.created) }}
            </template>
          </ElTableColumn> -->
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
          <ElDivider class="mx-8px" content-position="left" style="margin-top: 36px;"><span style="font-weight: bold;">清仓记录</span></ElDivider>
    <ElRow>
        <ElCol :span="24" style="text-align: right;">
            <ElButton @click="showSoldoutTable = !showSoldoutTable">显示/隐藏</ElButton>
        </ElCol>
    </ElRow>
    <ElRow :gutter="24" v-if="showSoldoutTable">
      <ElTable
        :data="soldoutData"
        :row-key="getHoldingKey"
        :expand-row-keys="soldoutExpandRows"
        @expand-change="onSoldoutExpandChanged"
        stripe
        :border="true"
        :default-sort="{ prop: 'record.updated', order: 'descending' }"
      >
        <ElTableColumn type="index" width="40" />
        <ElTableColumn type="expand">
          <template #default="{ row }">
            <div class="mx-24px my-8px">
              <ElRow :gutter="24">
                <ElText tag="b">操作记录 ({{ row.items.filter(item => item.action === OPERATION_ACTION_SOLDOUT).length }})</ElText>
              </ElRow>
            </div>
            <div class="mx-24px my-8px">
              <ElTable
                size="small"
                :data="row.items.filter(item => item.action === OPERATION_ACTION_SOLDOUT)"
                stripe
                :border="true"
                :default-sort="{ prop: 'created', order: 'descending' }"
              >
                <ElTableColumn type="index" width="40" />
                <ElTableColumn label="操作" prop="action" width="80">
                  <template #default="{ row }">
                    <ElText
                      :class="
                        row.action == OPERATION_ACTION_BUY
                          ? 'red-text'
                          : row.action == OPERATION_ACTION_SELL
                            ? 'green-text'
                            : ''
                      "
                    >
                      {{
                        row.action == OPERATION_ACTION_BUY
                          ? '买入'
                          : row.action == OPERATION_ACTION_SELL
                            ? '卖出'
                            : row.action == OPERATION_ACTION_SOLDOUT
                              ? '清仓'
                              : '计息'
                      }}
                    </ElText>
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
              </ElTable>
            </div>
          </template>
        </ElTableColumn>
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
        <ElTableColumn label="盈亏" min-width="120">
          <template #default="{ row }">
            <ElText
              :class="row.calc?.profit >= 0 ? 'red-text' : 'green-text'"
            >
              {{ formatNumberString(row.calc?.profit) }}
            </ElText>
          </template>
        </ElTableColumn>
        <ElTableColumn label="数量" min-width="100">
          <template #default="{ row }">
            {{ formatNumberString(row.calc?.quantity) }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="价格" min-width="80">
          <template #default="{ row }">
            {{ formatNumberString(row.calc?.price) }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="操作时间" min-width="120">
          <template #default="{ row }">
            {{ formatToDateTime(row.calc?.date) }}
          </template>
        </ElTableColumn>
      </ElTable>
    </ElRow>    <ElDialog v-model="fundsDialogVisible" :destroy-on-close="true" width="25%">
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
        <ElButton @click="fundsDialogVisible = false">取消</ElButton>
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
        <ElButton @click="createDialogVisible = false">取消</ElButton>
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
              <ElCol :span="14">
                <ElRadioGroup v-model="operationForm.action">
                  <ElRadioButton :value="OPERATION_ACTION_BUY">买入</ElRadioButton>
                  <ElRadioButton :value="OPERATION_ACTION_SELL">卖出</ElRadioButton>
                  <ElRadioButton :value="OPERATION_ACTION_INTEREST">计息</ElRadioButton>
                </ElRadioGroup>
              </ElCol>
              <ElCol :span="10">
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
            <ElInput
              v-model.number="operationForm.quantity"
              :disabled="operationForm.action === OPERATION_ACTION_INTEREST"
            />
          </ElFormItem>
          <ElFormItem label="价格" @change="onPriceBlur">
            <ElInput
              v-model="operationForm.price"
              :disabled="operationForm.action === OPERATION_ACTION_INTEREST"
            >
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
        <ElButton @click="operationDialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="onAddOperation">确定</ElButton>
      </template>
    </ElDialog>
    <KLineDialog
      :visible="klineDialogVisible"
      :req-param="reqParam"
      @update:on-close="klineDialogVisible = false"
      width="60%"
    />
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
