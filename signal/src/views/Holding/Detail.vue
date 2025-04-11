<script setup lang="ts">
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElRow, ElTable, ElTableColumn } from 'element-plus'
import { OPERATION_ACTION_BUY } from '@/api/holding/types'
import { calcProfitTraceData, getHoldingData, OperationItem, ProfitTraceItem } from '@/calc/holding'
import { apiGetHistoryData, HistoryData } from '@/api/data'
import { HoldingItem } from '@/calc/holding'
import { apiOperationList } from '@/api/holding'
import * as Utils from '@/utils/dateUtil'
import DetailChart from './components/DetailChart.vue'

const { go } = useRouter()

const props = defineProps({
  id: {
    type: [String, Number],
    required: false
  }
})

const holdingData = ref<HoldingItem[]>()
const operationData = ref<OperationItem[]>([])
const historyData = ref<HistoryData[]>([])
const profitTraceData = ref<ProfitTraceItem[]>([])

const holding = computed(() => Number(props.id))

async function fetchData() {
  // holding
  holdingData.value = await getHoldingData(holding.value)
  console.log('holdingData', holdingData.value)
  // operation
  operationData.value = (await apiOperationList({holding: holding.value})).result as OperationItem[]
  operationData.value = operationData.value.reverse()
  // history
  let start = Utils.dateUtil(operationData.value[0].created)
  let end = Utils.dateUtil(operationData.value[operationData.value.length - 1].created)
  if (start.diff(end, 'month') < 3) {
    start = Utils.dateUtil(operationData.value[0].created).subtract(3, 'month')
    end = Utils.dateUtil(operationData.value[operationData.value.length - 1].created).add(3, 'month')
  }
  historyData.value = (await apiGetHistoryData({
    type: holdingData.value[0]!.type,
    code: holdingData.value[0]!.code,
    start: Utils.formatToDate(start),
    end: Utils.formatToDate(end)
  })).result as HistoryData[]
  // trace
  profitTraceData.value = calcProfitTraceData(operationData.value, historyData.value)
}

function getHistoryData(date: Date): HistoryData | undefined {
  return historyData.value.find(item => item.日期 === Utils.formatToDate(date))
}

onMounted(() => {
  fetchData().then(() => {
    // console.log('holdingData', holdingData.value)
    // console.log('operationData', operationData.value)
    // console.log('profitTraceData', profitTraceData.value)
  })
})

</script>

<template>
  <ContentDetailWrap style="height: 300px;">
    <template #header>
      <ElButton type="primary" @click="go(-1)">返回</ElButton>
      <!-- <ElButton type="primary" @click="onTest">Test</ElButton> -->
    </template>
    <ElRow :gutter="24">
      <ElTable :data="holdingData" stripe :border="true">
        <ElTableColumn prop="code" label="代码" min-width="80" />
        <ElTableColumn prop="name" label="名称" min-width="80" />
        <!-- <ElTableColumn prop="flag" label="Flag" width="50" /> -->
        <ElTableColumn prop="quantity" label="数量" min-width="60" />
        <ElTableColumn prop="expense" label="成本" min-width="60" />
        <ElTableColumn prop="price_avg" label="均价" min-width="80" />
        <ElTableColumn prop="price_cur" label="现价" min-width="80">
          <template #default="{ row }">
            {{ `${row.price_cur}[${row.price_date.substring(5)}]` }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="revenue" label="收益" min-width="80" />
        <ElTableColumn prop="profit" label="利润" min-width="80" />
        <ElTableColumn prop="profit_rate" label="利润率 %" min-width="100" />
        <ElTableColumn prop="created" label="创建时间" min-width="120">
          <template #default="{ row }">
            {{ Utils.formatToDate(row.created) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="updated" label="更新时间" min-width="120">
          <template #default="{ row }">
            {{ Utils.formatToDate(row.updated) }}
          </template>
        </ElTableColumn>
      </ElTable>
    </ElRow>
    <ElRow :gutter="24">
      <DetailChart :profitData="profitTraceData" :historyData="historyData" :width="'100%'" :height="'500px'" />
    </ElRow>
    <ElRow :gutter="24">
      <ElTable :data="operationData" stripe :border="true">
        <ElTableColumn type="index" width="40" />
        <ElTableColumn label="操作" prop="action" width="60">
          <template #default="{ row }"> 
            {{ row.action == OPERATION_ACTION_BUY ? '买入' : '卖出' }}
          </template> 
        </ElTableColumn>
        <ElTableColumn label="数量" prop="quantity" min-width="80" />
        <ElTableColumn label="买入/卖出" prop="price" min-width="80" />
        <ElTableColumn label="收盘价" min-width="80">
          <template #default="{ row }">
            {{ getHistoryData(row.created)?.收盘 }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="费用" prop="expense" min-width="80" />
        <ElTableColumn label="操作时间" prop="created" min-width="120">
          <template #default="{ row }">
            {{ Utils.formatToDateTime(row.created) }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="备注" prop="comment" />
      </ElTable>
    </ElRow>
  </ContentDetailWrap>
</template>

