<script setup lang="ts">
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElRow, ElTable, ElTableColumn } from 'element-plus'
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
  // history
  const start = Utils.formatToDate(operationData.value[0].created)
  const end = Utils.formatToDate(operationData.value[operationData.value.length - 1].created)
  historyData.value = (await apiGetHistoryData({
    type: holdingData.value[0]!.type,
    code: holdingData.value[0]!.code,
    start: start,
    end: end
  })).result as HistoryData[]
  // trace
  profitTraceData.value = calcProfitTraceData(operationData.value, historyData.value)
}

onMounted(() => {
  fetchData().then(() => {
    console.log('holdingData', holdingData.value)
    console.log('operationData', operationData.value)
    console.log('profitTraceData', profitTraceData.value)
  })
})

async function onTest() {

}

</script>

<template>
  <ContentDetailWrap title="Operation">
    <template #header>
      <ElButton type="primary" @click="go(-1)">返回</ElButton>
      <ElButton type="primary" @click="onTest">Test</ElButton>
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
  </ContentDetailWrap>
</template>

