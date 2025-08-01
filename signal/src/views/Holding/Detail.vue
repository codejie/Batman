<script setup lang="ts">
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { computed, onMounted, PropType, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElRow, ElTable, ElTableColumn, ElText } from 'element-plus'
import { calcProfitData, calcProfitTraceData, getHoldListData, HoldingListItem, ProfitTraceItem } from '@/calc/holding'
import { apiGetHistoryData, HistoryDataItem } from '@/api/data'
import * as Utils from '@/utils/dateUtil'
import DetailChart from './components/DetailChart.vue'
import { KLineDialog } from '@/components/KLine'
import { HoldingRecordItem } from '@/api/holding'
import { formatNumberString, formatRateString } from '@/utils/fmtUtil'

const { go } = useRouter()

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  ids: {
    type: String,
    required: true
  }
})

const holdingId = ref<number>(Number(props.id))
const holdingIds =  ref<number[]>(props.ids.split(',').map(id => Number(id)))

const holdingData = ref<HoldingListItem[]>()
const historyData = ref<HistoryDataItem[]>([])
const profitTraceData = ref<ProfitTraceItem[]>([])
const profitTableToggle = ref<boolean>(false) // false: only show operation data, true: show operation trace data
const profitTableData = ref<ProfitTraceItem[]>([])
const profitTableExpanded = ref<boolean>(false)

const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<any>({})

async function fetchData(id) {
  // holding
  holdingData.value = await getHoldListData(id)
  
  const operationData = holdingData.value[0]?.items ?? []
  if (operationData.length > 0) {
    // history
    let start = Utils.dateUtil(operationData[0].created)
    let end = Utils.dateUtil(operationData[operationData.length - 1].created)
    if (start.diff(end, 'month') < 3) {
      start = Utils.dateUtil(operationData[0].created).subtract(3, 'month')
      end = Utils.dateUtil(operationData[operationData.length - 1].created).add(3, 'month')
    }
    const historyRet = await apiGetHistoryData({
      type: holdingData.value[0]!.record.type,
      code: holdingData.value[0]!.record.code,
      start: Utils.formatToDate(start),
      end: Utils.formatToDate(end)
    })
    historyData.value = historyRet.result
    // trace
    profitTraceData.value = calcProfitTraceData(operationData, historyData.value)
    if (profitTableToggle.value) {
      profitTableData.value = profitTraceData.value//.reverse()
    } else {
      profitTableData.value = calcProfitData(operationData, historyData.value)
    }
    // profitTableData.value = profitTableData.value.reverse()
  } else {
    const end = Utils.dateUtil()
    const start = Utils.dateUtil().subtract(3, 'month')
    const historyRet = await apiGetHistoryData({
      type: holdingData.value[0]!.record.type,
      code: holdingData.value[0]!.record.code,
      start: Utils.formatToDate(start),
      end: Utils.formatToDate(end)
    })
    historyData.value = historyRet.result    
  }
}

function onProfitTableShow() {
  profitTableToggle.value = !profitTableToggle.value
  if (holdingData.value && holdingData.value.length >0) {
    if (profitTableToggle.value) {
        profitTableData.value = profitTraceData.value
    } else {
      if (holdingData.value && holdingData.value.length > 0)
        profitTableData.value = calcProfitData(holdingData.value[0].items!, historyData.value)
      else
        profitTableData.value = []
    }
  }
  // profitTableData.value = profitTableData.value.reverse()
}

function profitTableTitle(): string {
  if (profitTableToggle.value) {
    return `跟踪记录(${profitTableData.value.length})`
  } else {
    return `操作记录(${profitTableData.value.length})`
  }
}

onMounted(() => {
  fetchData(holdingId.value).then(() => {})
})

function onRecordClick(row: HoldingRecordItem) {
  reqParam.value = {
    code: row.code,
    name: row.name,
    type: row.type,
    // start: row.created,
    // end: new Date()
  }
  klineDialogVisible.value = true
}

function onKLineDialogClose() {
  klineDialogVisible.value = false
}

function checkPrev(): boolean {
  if (holdingIds.value.length == 1) {
    return true
  }
  return holdingIds.value.indexOf(holdingId.value) == 0
}

function checkNext(): boolean {
  if (holdingIds.value.length == 1) {
    return true
  }
  return holdingIds.value.indexOf(holdingId.value) == holdingIds.value.length - 1
}

async function onPrev() {
  holdingId.value = holdingIds.value![holdingIds.value!.indexOf(holdingId.value) - 1]
  await fetchData(holdingId.value)
}

async function onNext() {
  holdingId.value = holdingIds.value![holdingIds.value!.indexOf(holdingId.value) + 1]
  await fetchData(holdingId.value)
}

function onProfitTableExpandChange(row, expandedRows) {
  profitTableExpanded.value = expandedRows.length > 0
}

</script>

<template>
  <ContentDetailWrap style="height: 300px;">
    <template #header>
      <ElButton type="primary" @click="go(-1)">返回</ElButton>
      <!-- <ElButton type="primary" @click="onTest">Test</ElButton> -->
       <div style="float: right; margin-right: 16px;">
        <ElButton :disabled="checkPrev()" @click="onPrev()">上一个</ElButton>
        <ElButton :disabled="checkNext()" @click="onNext()">下一个</ElButton>
       </div>
    </template>
    <ElRow :gutter="24">
      <ElTable :data="holdingData" stripe :border="true" :default-expand-all="profitTableExpanded"  @expand-change="onProfitTableExpandChange">
        <ElTableColumn type="expand">
          <div class="mx-4px my-4px">
            <ElButton size="small" class="mx-8" type="primary" @click="onProfitTableShow()">{{ profitTableTitle() }}</ElButton>
          </div>
          <div class="mx-24px my-8px">
            <ElTable :data="profitTableData" stripe :border="true" :default-sort="{ prop: 'date', order: 'descending' }">
              <ElTableColumn  type="index" width="50" />
              <ElTableColumn prop="date" label="日期" min-width="60" />
              <ElTableColumn prop="quantity" label="操作" min-width="50" />
              <ElTableColumn prop="price" label="买入" min-width="60">
                <template #default="{ row }">
                  {{ formatNumberString(row.price) }}
                </template>
              </ElTableColumn>
              <ElTableColumn label="成本" min-width="60">
                <template #default="{ row }">
                  {{ formatNumberString(row.expense) }}
                </template>
              </ElTableColumn>
              <ElTableColumn prop="holding" label="持有" min-width="60" />              
              <ElTableColumn label="总额" min-width="80">
                <template #default="{ row }">
                  {{ formatNumberString(row.amount) }}
                </template>
              </ElTableColumn>              
              <ElTableColumn label="均价" min-width="60">
                <template #default="{ row }">
                  {{ formatNumberString(row.price_avg) }}
                </template>
              </ElTableColumn>
              <ElTableColumn prop="price_close" label="时价" min-width="60" />
              <ElTableColumn label="市值" min-width="80">
                <template #default="{ row }">
                  {{ formatNumberString(row.revenue) }}
                </template>
              </ElTableColumn>
              <ElTableColumn label="盈亏" min-width="80">
                <template #default="{ row }">
                  <div :class="row.profit < 0 ? 'green-text' : 'red-text'">
                    {{ formatNumberString(row.profit) }}
                  </div>
                </template>
              </ElTableColumn>
              <ElTableColumn label="盈亏率 %" min-width="100">
                <template #default="{ row }">
                  <div :class="row.profit_rate < 0 ? 'green-text' : 'red-text'">
                    {{ formatRateString(row.profit_rate) }}
                  </div>
                </template>
              </ElTableColumn>
              <ElTableColumn label="昨差" min-width="80">
                <template #default="{ row }">
                  <div :class="row.pre_profit_diff > 0 ? 'red-text' : (row.pre_profit_diff < 0 ? 'green-text' : '')">
                    {{ formatNumberString(row.pre_profit_diff)}}
                  </div>
                </template>
              </ElTableColumn>
              <ElTableColumn label="昨差率 %" min-width="100">
                <template #default="{ row }">
                  <div :class="row.pre_profit_rate > 0 ? 'red-text' : (row.pre_profit_rate < 0 ? 'green-text' : '')">
                    {{ formatRateString(row.pre_profit_rate) }}
                  </div>
                </template>
              </ElTableColumn>              
            </ElTable>            
          </div>
        </ElTableColumn>
        <ElTableColumn prop="record.code" label="代码" min-width="80">
          <template #default="{ row }">
            <ElText tag="b" @click="onRecordClick(row.record)">{{ row.record.code }}</ElText>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="record.name" label="名称" min-width="80" />
        <!-- <ElTableColumn prop="flag" label="Flag" width="50" /> -->
        <ElTableColumn prop="record.quantity" label="持有" min-width="60" />
        <ElTableColumn prop="record.expense" label="成本" min-width="60" />
        <ElTableColumn prop="calc?.price_avg" label="均价" min-width="80">
          <template #default="{ row }">
            {{ formatNumberString(row.calc?.price_avg) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc?.price_cur" label="现价/日期" min-width="80">
          <template #default="{ row }">
            {{ formatNumberString(row.calc?.price_cur) }} [{{ `${row.calc?.date_cur.substring(5)}` }}]
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc?.revenue" label="市值" min-width="80">
          <template #default="{ row }">
            {{ formatNumberString(row.calc?.revenue) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc?.profit" label="盈亏" min-width="80">
          <template #default="{ row }">
            <div :class="row.calc?.profit < 0 ? 'green-text' : 'red-text'">
              {{ formatNumberString(row.calc?.profit) }}
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc?.profit_rate" label="盈亏率 %" min-width="100">
          <template #default="{ row }">
            <div :class="row.calc?.profit_rate < 0 ? 'green-text' : 'red-text'">
              {{ formatRateString(row.calc?.profit_rate) }}
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="record.created" label="创建时间" min-width="120">
          <template #default="{ row }">
            {{ Utils.formatToDate(row.record.created) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="record.updated" label="更新时间" min-width="120">
          <template #default="{ row }">
            {{ Utils.formatToDate(row.record.updated) }}
          </template>
        </ElTableColumn>
      </ElTable>
    </ElRow>
    <ElRow :gutter="24">
      <DetailChart :history-data="historyData" :profit-data="profitTraceData" :width="'100%'" :height="'630px'" />
    </ElRow>
    <KLineDialog :visible="klineDialogVisible" :req-param="reqParam" @update:on-close="onKLineDialogClose" width="60%" />    
  </ContentDetailWrap>
</template>
<style lang="css" scoped>
.green-text {
    color: green;
}

.red-text {
    color: red;
}
</style>
