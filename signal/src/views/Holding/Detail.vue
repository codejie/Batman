<script setup lang="ts">
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton, ElRow, ElTable, ElTableColumn } from 'element-plus'
import { calcProfitTraceData, getHoldListData, HoldingListItem, ProfitTraceItem } from '@/calc/holding'
import { apiGetHistoryData, HistoryData } from '@/api/data'
import * as Utils from '@/utils/dateUtil'
import DetailChart from './components/DetailChart.vue'

const { go } = useRouter()

const props = defineProps({
  id: {
    type: [String, Number],
    required: false
  }
})

const holdingData = ref<HoldingListItem[]>()
// const operationData = ref<OperationItem[]>([])
const historyData = ref<HistoryData[]>([])
const profitTraceData = ref<ProfitTraceItem[]>([])
const profitTableData = ref<ProfitTraceItem[]>([]) 

const holding = computed(() => Number(props.id))

async function fetchData() {
  // holding
  holdingData.value = await getHoldListData(holding.value)
  
  const operationData = holdingData.value[0]!.items
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
    console.log('operationData', operationData)
    profitTraceData.value = calcProfitTraceData(operationData, historyData.value)
    profitTableData.value = profitTraceData.value.filter(item => !item.is_filled).reverse()
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

onMounted(() => {
  fetchData().then(() => {})
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
              <ElTableColumn prop="date" label="日期" min-width="80" />
              <ElTableColumn prop="quantity" label="操作" min-width="60" />
              <ElTableColumn prop="holding" label="持有" min-width="60" />
              <ElTableColumn label="成本" min-width="60">
                <template #default="{ row }">
                  {{ row.expense.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn label="均价" min-width="80">
                <template #default="{ row }">
                  {{ row.price_avg.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn prop="price" label="时价" min-width="80" />
              <ElTableColumn label="市值" min-width="80">
                <template #default="{ row }">
                  {{ row.revenue.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn label="盈亏" min-width="80">
                <template #default="{ row }">
                  {{ row.profit?.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn label="盈亏率 %" min-width="100">
                <template #default="{ row }">
                  {{ (row.profit_rate * 100)?.toFixed(2) + '%' }}
                </template>
              </ElTableColumn>
              <ElTableColumn label="昨差" min-width="100">
                <template #default="{ row }">
                  {{ row.pre_profit?.toFixed(2) }}
                </template>
              </ElTableColumn>
              <ElTableColumn label="昨差率 %" min-width="100">
                <template #default="{ row }">
                  {{ row.pre_profit_rate ? (row.pre_profit_rate * 100).toFixed(2) + '%' : '-'}}
                </template>
              </ElTableColumn>              
            </ElTable>            
          </div>
        </ElTableColumn>
        <ElTableColumn prop="record.code" label="代码" min-width="80" />
        <ElTableColumn prop="record.name" label="名称" min-width="80" />
        <!-- <ElTableColumn prop="flag" label="Flag" width="50" /> -->
        <ElTableColumn prop="record.quantity" label="持有" min-width="60" />
        <ElTableColumn prop="record.expense" label="成本" min-width="60" />
        <ElTableColumn prop="calc.price_avg" label="均价" min-width="80">
          <template #default="{ row }">
            {{ `${row.calc.price_avg? row.calc.price_avg.toFixed(2) : '-'}` }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc.price_cur" label="现价" min-width="80">
          <template #default="{ row }">
            {{ `${row.calc.price_cur} | ${row.calc.date_cur.substring(5)}` }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc.revenue" label="市值" min-width="80">
          <template #default="{ row }">
            {{ `${row.calc.revenue? row.calc.revenue.toFixed(2) : '-'}` }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc.profit" label="盈亏" min-width="80">
          <template #default="{ row }">
            {{ `${row.calc.profit? row.calc.profit.toFixed(2) : '-'}` }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="calc.profit_rate" label="盈亏率 %" min-width="100">
          <template #default="{ row }">
            {{ `${row.calc.profit_rate? (row.calc.profit_rate * 100).toFixed(2) + '%' : '-'}` }}
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
      <DetailChart :history-data="historyData" :profit-data="profitTraceData" :width="'100%'" :height="'500px'" />
    </ElRow>
  </ContentDetailWrap>
</template>

