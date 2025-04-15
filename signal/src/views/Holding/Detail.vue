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
const profitTableData = ref<ProfitTraceItem[]>([]) 

const holding = computed(() => Number(props.id))

async function fetchData() {
  // holding
  holdingData.value = await getHoldingData(holding.value)
  // operation
  operationData.value = (await apiOperationList({holding: holding.value})).result as OperationItem[]
  console.log(operationData.value)
  // operationData.value = operationData.value.reverse()
  // history
  let start = Utils.dateUtil(operationData.value[0].created)
  let end = Utils.dateUtil(operationData.value[operationData.value.length - 1].created)
  if (start.diff(end, 'month') < 3) {
    start = Utils.dateUtil(operationData.value[0].created).subtract(3, 'month')
    end = Utils.dateUtil(operationData.value[operationData.value.length - 1].created).add(3, 'month')
  }
  console.log('===============', start, end)
  const historyRet = await apiGetHistoryData({
    type: holdingData.value[0]!.type,
    code: holdingData.value[0]!.code,
    start: Utils.formatToDate(start),
    end: Utils.formatToDate(end)
  })
  historyData.value = historyRet.result
  // trace
  profitTraceData.value = calcProfitTraceData(operationData.value, historyData.value)
  profitTableData.value = profitTraceData.value.filter(item => !item.is_filled).reverse()
}

// function getHistoryData(date: Date): HistoryData | undefined {
//   return historyData.value.find(item => item.日期 === Utils.formatToDate(date))
// }

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
        <ElTableColumn type="expand">
          <div class="mx-24px my-8px">
            <ElTable :data="profitTableData" stripe :border="true">
              <ElTableColumn  type="index" width="40" />
              <ElTableColumn prop="date" label="日期" min-width="120" />
              <ElTableColumn prop="quantity" label="操作" min-width="60" />
              <ElTableColumn prop="holding" label="持有" min-width="60" />
              <ElTableColumn prop="expense" label="成本" min-width="60">
                <template #default="{ row }">
                  {{ row.expense.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn prop="price_avg" label="均价" min-width="80">
                <template #default="{ row }">
                  {{ row.price_avg.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn prop="price" label="时价" min-width="80" />
              <ElTableColumn prop="revenue" label="市值" min-width="80">
                <template #default="{ row }">
                  {{ row.revenue.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn prop="profit" label="盈亏" min-width="80">
                <template #default="{ row }">
                  {{ row.profit.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn prop="profit_rate" label="盈亏率 %" min-width="100">
                <template #default="{ row }">
                  {{ row.profit_rate.toFixed(2) + '%' }}
                </template>
              </ElTableColumn>
            </ElTable>            
          </div>
        </ElTableColumn>
        <ElTableColumn prop="code" label="代码" min-width="80" />
        <ElTableColumn prop="name" label="名称" min-width="80" />
        <!-- <ElTableColumn prop="flag" label="Flag" width="50" /> -->
        <ElTableColumn prop="holding" label="持有" min-width="60" />
        <ElTableColumn prop="expense" label="成本" min-width="60" />
        <ElTableColumn prop="price_avg" label="均价" min-width="80" />
        <ElTableColumn prop="price_cur" label="现价" min-width="80">
          <template #default="{ row }">
            {{ `${row.price_cur}[${row.price_date.substring(5)}]` }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="revenue" label="市值" min-width="80" />
        <ElTableColumn prop="profit" label="盈亏" min-width="80" />
        <ElTableColumn prop="profit_rate" label="盈亏率 %" min-width="100" />
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
      <DetailChart :history-data="historyData" :profit-data="profitTraceData" :width="'100%'" :height="'500px'" />
    </ElRow>
  </ContentDetailWrap>
</template>

