<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn, ElDropdown, ElDropdownMenu, ElDropdownItem, ElInput, ElText, ElMessage } from 'element-plus'
import { KLineChart4 } from '@/components/KLine'
import { onMounted, ref, unref, watch } from 'vue';
import { apiHistory, apiInfo } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { calcMAData, getKLineDataRange, KLineChartData, KLineData, MACDData, MAData, makeKLineChartData, makeMACDData, VolumeData, XData } from '@/utils/kline';
import { apiMACD } from '@/api/libs/talib';

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
const itemFetched = ref<boolean>(false)
const itemTitleOutput = ref<string>()
const itemDataOutput = ref<string>()
const maSelected = ref<number[]>([])
const secondMode = ref<string>('Volume')

let itemCode: ItemCode
let baseItem: ItemContext
let moreItems: ItemContext[]

let k_zoom: boolean = false
let k_line: boolean = true

let searchTimer: NodeJS.Timeout
watch(
  () => inputCode.value,
  async () => {
    if (!inputCode.value || inputCode.value.length < 6)
      return

    clearTimeout(searchTimer)
    searchTimer = setTimeout(async () => {
      await fetchItemCode(inputCode.value!)
    }, 1000)
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

function setKLine(item: ItemCode, chart, data: KLineData) {
  const name = item.code + '-K'
  if (k_line) {
    chart?.addKLine(0, name, data, true, true)
  } else {
    kchart.value?.remove(name)
  }
}

async function fetchItemCode(code: string) {
  itemTitleOutput.value = ''
  itemDataOutput.value = ''
  itemFetched.value = false
  
  const ret = await apiInfo({
    code: code
  })
  if (ret.result) {
    itemFetched.value = true
    itemCode = {
      type: codeType.value == 'Stock' ? 1 : 0,
      code: ret.result.code,
      name: ret.result.name
    }
    itemTitleOutput.value = `${itemCode.code}(${itemCode.name}):  `
    const hret = await apiHistory({
      code: itemCode.code
    })
    if (hret.result.length > 0) {
      itemDataOutput.value = makeItemDataOutput(hret.result[0])        
    }
  }
}

async function fetchItemMACDData(code: string, xData: XData, klineData: KLineData): Promise<MACDData> {
  const closeData = klineData.map(item => item[1])
  const ret = await apiMACD({
    value: (closeData as number[])
  })
  return makeMACDData(xData, ret.result.data)
}

function makeItemDataOutput(data: HistoryDataModel) {
  return `${data.date}\
  | 现价: ${data.price}\
  | 涨跌幅: ${data.percentage}%\
  | 涨跌额: ${data.amount}\
  | 振幅: ${data.volatility}%\
  | 今开: ${data.open}\
  | 昨收: ${data.close}\
  | 最高: ${data.high}\
  | 最低: ${data.low}\
  | 成交量: ${data.volume}\
  | 成交额: ${data.turnover}\
  | 换手率: ${data.rate}%`
}

function makeReqStart(range: string): string {
  return '2023-01-01'
}

async function makeItemContext(item: ItemCode, historyData: HistoryDataModel[]) {
  const context: ItemContext = {
    item: item,
    historyData: historyData,
    chartData: makeKLineChartData(historyData)    
  }
  makeItemContextMAData(maSelected.value, context)

  if (baseItem) {
    moreItems.push(context)
    drawMoreItem(context)
  } else {
    baseItem = context
    await drawBaseItem(context)
  }
}

function makeItemContextMAData(maSelected: number[], context: ItemContext) {
  context.chartData.maData = {}
  maSelected.forEach(item => {
    context.chartData.maData[item] = calcMAData(item, context.chartData.xData, context.chartData.klineData)
  })
}

async function drawBaseItem(context: ItemContext) {
  itemTitleOutput.value = `${context.item.code}(${context.item.name}):  `
  itemDataOutput.value = makeItemDataOutput(context.historyData[context.historyData.length - 1])

  setAxis(kchart.value, context.chartData.xData)
  setKLine(context.item, kchart.value, context.chartData.klineData)
  if (secondMode.value == 'Volume') {
    setSecondVolume(context.item, kchart.value, context.chartData.volumeData)
  } else {
    if (!context.chartData.macdData) {
      context.chartData.macdData = await fetchItemMACDData(context.item.code, context.chartData.xData, context.chartData.klineData)
    }
    setSecondMACD(context.item, kchart.value, context.chartData.macdData)
  }
}

function onCodeTypeCommand(cmd: string) {
  codeType.value = cmd
}

function onItemAddClick() {
  if (itemCode) {
    if (codeList.value.indexOf(itemCode) == -1) {
      codeList.value.push(itemCode)
    } else {
      ElMessage({
        message: `${itemCode.code} has been in list.`,
        type: 'warning',
      })      
    }
  }
}

// async function onCodeListClick(row: ItemCode) {
//   const ret = await apiHistory({
//     code: row.code,
//     start: makeReqStart('')
//   })
//   makeItemContext(row, ret.result)
//   // setChart(ret.result)
// }

async function onCodeListSelected(selected: ItemCode[], row: ItemCode) {
  console.log(selected)
  console.log(row)
  if (selected.includes(row)) {
    const ret = await apiHistory({
      code: row.code,
      start: makeReqStart('')
    })
    makeItemContext(row, ret.result)
  } else {
    removeItemContext(row)
  }
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
        <ElButton type="primary" :disabled="!itemFetched" @Click="onItemAddClick">+</ElButton>
        <ElText tag="b" size="default">{{ itemTitleOutput }}</ElText>
        <ElText size="default">{{ itemDataOutput }}</ElText>
      </ElCol>
    </ElRow>
    <ElRow class="row" :gutter="24">
      <ElCol :span="3">
        <ElTable :data="codeList" size="small" @select="onCodeListSelected" :border="true" max-height="800" highlight-current-row>
          <ElTableColumn type="selection" width="30" />
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
