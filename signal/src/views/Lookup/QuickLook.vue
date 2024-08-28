<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn, ElDropdown, ElDropdownMenu, ElDropdownItem, ElInput, ElText, ElMessage } from 'element-plus'
import { KLineChart4 } from '@/components/KLine'
import { onMounted, ref, unref, watch } from 'vue';
import { apiHistory, apiInfo } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { getKLineDataRange, KLineChartData, KLineData, makeKLineChartData, VolumeData, XData } from '@/utils/kline';

type ItemCode = {
  type?: number
  code: string
  name?: string
}

type ItemContext = {
  item: ItemCode
  historyData: HistoryDataModel[]
  chartData: KLineChartData
}

const props = defineProps({
  code: {
    type: String,
    required: false
  }
})

const kchart = ref(null)
const codeType = ref<string>('Stock')
const codeList = ref<ItemCode[]>([])
const inputCode = ref<string>()
const itemCode = ref<ItemCode>()
const itemHistoryData = ref<HistoryDataModel>()
const itemTitleOutput = ref<string>()
const itemDataOutput = ref<string>()

let baseItem: ItemContext
let moreItem: ItemContext[]


let k_zoom: boolean = false
let chartData: KLineChartData

let searchTimer: NodeJS.Timeout
watch(
  () => inputCode.value,
  async () => {
    if (!inputCode.value || inputCode.value.length < 6)
      return

    clearTimeout(searchTimer)
    searchTimer = setTimeout(async () => {
        itemTitleOutput.value = ''
        itemDataOutput.value = ''
        itemCode.value = undefined
        
        const ret = await apiInfo({
        code: inputCode.value!
      })
      if (ret.result) {
        itemCode.value = {
          type: codeType.value == 'Stock' ? 1 : 0,
          code: ret.result.code,
          name: ret.result.name
        }
        itemTitleOutput.value = `${unref(itemCode)?.code}(${unref(itemCode)?.name}):  ` 
      }
    }, 1000)
  }
)

watch(
  () => itemCode.value,
  async () => {
    if (itemCode.value) {
        const ret = await apiHistory({
        code: itemCode.value!.code
      })

      if (ret.result.length > 0) {
        itemHistoryData.value = ret.result[0]
        itemDataOutput.value = makeItemData()
      }
    }
  }
)

onMounted(() => {
  setGrid(kchart.value)
  if (props.code) {
    inputCode.value = props.code
  }
})

function setGrid(chart) {
  chart?.reset()
  if (k_zoom) {
    chart?.addGrid(0, '4%', '4%', '4%', '10%')
  } else {
    chart?.addGrid(0, '4%', '4%', '4%', '40%')
    chart?.addGrid(1, '4%', '70%', '4%', '6%')
  }
}

function setAxis(chart, data: XData) {
  if (k_zoom) {
    chart?.addAxis(0, data, true)
    chart?.addAxisPointer([0])
  } else {
    chart?.addAxis(0, data, true)
    chart?.addAxis(1, data, false)
    chart?.addAxisPointer([0, 1])
  }
}

function setKLine(chart, data: KLineData) {
  // if (kline) {
    chart?.addKLine(0, 'KLine', data, true, true)
  // } else {
  //   kchart.value?.remove('KLine')
  // }
}

function makeItemData() {
  return `${unref(itemHistoryData)?.date}\
  | 现价: ${unref(itemHistoryData)?.price}\
  | 涨跌幅: ${unref(itemHistoryData)?.percentage}%\
  | 涨跌额: ${unref(itemHistoryData)?.amount}\
  | 振幅: ${unref(itemHistoryData)?.volatility}%\
  | 今开: ${unref(itemHistoryData)?.open}\
  | 昨收: ${unref(itemHistoryData)?.close}\
  | 最高: ${unref(itemHistoryData)?.high}\
  | 最低: ${unref(itemHistoryData)?.low}\
  | 成交量: ${unref(itemHistoryData)?.volume}\
  | 成交额: ${unref(itemHistoryData)?.turnover}\
  | 换手率: ${unref(itemHistoryData)?.rate}%`
}

function makeReqStart(range: string): string {
  return '2023-01-01'
}

function makeItemContext(item: ItemCode, historyData: HistoryDataModel[]) {
  if (baseItem) {

  } else {
    baseItem = {
      item: item,
      historyData: historyData,
      chartData: makeKLineChartData(historyData)
    }
  }
}

function setChart(historyData: HistoryDataModel[]) {
  
  chartData = makeKLineChartData(historyData)

  getKLineDataRange(chartData.klineData)

  setAxis(kchart.value, chartData.xData)
  setKLine(kchart.value, chartData.klineData)
}

function onCodeTypeCommand(cmd: string) {
  codeType.value = cmd
}

function onItemAddClick() {
  if (itemCode.value) {
    if (codeList.value.indexOf(itemCode.value) == -1) {
      codeList.value.push(itemCode.value)
    } else {
      ElMessage({
        message: `${itemCode.value.code} has been in list.`,
        type: 'warning',
      })      
    }
  }
}

async function onCodeListClick(row: ItemCode) {
  const ret = await apiHistory({
    code: row.code,
    start: makeReqStart('')
  })
  makeItemContext(row, ret.result)
  // setChart(ret.result)
}

</script>
<template>
  <ContentWrap title="Lookup">
    <ElRow class="row" :gutter="24">
      <ElCol :span="24">
        <ElDropdown trigger="click" @command="onCodeTypeCommand">
          <ElButton>{{ codeType }}</ElButton>
          <template #dropdown>
            <ElDropdownMenu>
              <ElDropdownItem command="Stock">Stock</ElDropdownItem>
              <ElDropdownItem command="Index">Index</ElDropdownItem>
            </ElDropdownMenu>
          </template>
        </ElDropdown>
        <ElInput v-model="inputCode" style="width: 80px;" max-length="6"/>
        <ElButton type="primary" :disabled="itemCode == undefined" @Click="onItemAddClick">+</ElButton>
        <ElText tag="b" size="default">{{ itemTitleOutput }}</ElText>
        <ElText size="default">{{ itemDataOutput }}</ElText>
      </ElCol>
    </ElRow>
    <ElRow class="row" :gutter="24">
      <ElCol :span="3">
        <ElTable :data="codeList" size="small" @row-click="onCodeListClick" :border="true" max-height="800" highlight-current-row>
          <ElTableColumn prop="code" label="Code" />
          <ElTableColumn prop="name" label="Name" />
          <!-- <ElTableColumn label="Action" /> -->
        </ElTable>
      </ElCol>
      <ElCol :span="21">
        <ElRow class="row" :gutter="24">
          <div>aaa</div>
        </ElRow>
        <KLineChart4 class="row" ref="kchart" />
      </ElCol>
    </ElRow>
  </ContentWrap>
</template>
<style lang="css">
.row {
  padding: 4px;
  outline: 1px solid gray;
}
</style>
