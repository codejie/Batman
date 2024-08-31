<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn, ElDropdown, ElDropdownMenu, ElDropdownItem, ElInput, ElText, ElMessage } from 'element-plus'
import { KLineChart4 } from '@/components/KLine'
import { onMounted, ref, unref, watch } from 'vue';
import { apiHistory, apiInfo } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { calcMAData, KLineChartData, KLineData, MACDData, MAData, MADataGroup, makeKLineChartData, makeMACDData, makeMADataGroup, VolumeData, XData } from '@/utils/kline';
import { apiMACD } from '@/api/libs/talib';
import { ka_GE } from '@faker-js/faker';

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
const maSelected = ref<number[]>([5, 10])
const secondMode = ref<string>('MACD')

let itemCode: ItemCode
let baseItem: ItemContext
let moreItems: ItemContext[] = []

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
    chart?.addKLine(0, name, data.data, true, true)
  } else {
    kchart.value?.remove(name)
  }
}

function setVolume(item: ItemCode, chart, data: VolumeData) {
  if (!k_zoom) {
    const name = item.code + '-V'
    chart.addBar(1, name, data.data)
  }
}

function setMACD(item: ItemCode, chart, data: MACDData) {
  chart.addLine(1, item.code + '-DIF', data.dif)
  chart.addLine(1, item.code + '-DEA', data.dea)
  chart.addBar(1, item.code + '-MACD', data.macd) 
}

function setMAData(item: ItemCode, chart, data: MADataGroup) {
  for (const key of Object.keys(data)) {
    const name = item.code + '-' + key
    chart.addLine(0, name, data[key].data)
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

async function calcItemMACDData( xData: XData, klineData: KLineData): Promise<MACDData> {
  const closeData = klineData.data.map(item => item[1])
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

function checkItemContext(item: ItemCode): boolean {
  if (baseItem && baseItem.item.code == item.code)
    return true
  for (let i = 0; i < moreItems.length; ++ i) {
    if (moreItems[i].item.code == item.code)
      return true
  }
  return false
}

async function makeItemContext(item: ItemCode) {
  if (checkItemContext(item)) return

  const ret = await apiHistory({
      code: item.code,
      start: makeReqStart('')
  })

  const historyData = ret.result
  const context: ItemContext = {
    item: item,
    historyData: historyData,
    chartData: makeKLineChartData(historyData)    
  }
  makeItemContextMAData(maSelected.value, context)
  
  if (baseItem) {
    moreItems.push(context)
  } else {
    baseItem = context
  }
}

function makeItemContextMAData(maSelected: number[], context: ItemContext) {
  context.chartData.maData = {}
  maSelected.forEach(item => {
    context.chartData.maData[item] = calcMAData(item, context.chartData.xData, context.chartData.klineData)
  })
}

async function drawItemContext() {
  await drawBaseItem()
  await drawMoreItems()
}

async function drawBaseItem() {
  const context = baseItem
  itemTitleOutput.value = `${context.item.code}(${context.item.name}):  `
  itemDataOutput.value = makeItemDataOutput(context.historyData[context.historyData.length - 1])

  setGrid(kchart.value)
  setAxis(kchart.value, context.chartData.xData)
  setKLine(context.item, kchart.value, context.chartData.klineData)
  if (!context.chartData.maData) {
    context.chartData.maData = makeMADataGroup(maSelected.value, context.chartData)
  }
  setMAData(context.item, kchart.value, context.chartData.maData)
  if (secondMode.value == 'Volume') {
    setVolume(context.item, kchart.value, context.chartData.volumeData)
  } else {
    if (!context.chartData.macdData) {
      context.chartData.macdData = await calcItemMACDData(context.chartData.xData, context.chartData.klineData)
    }
    setMACD(context.item, kchart.value, context.chartData.macdData)
  }
}

async function drawMoreItems() {

}

function clearItemContext(item: ItemCode) {
  kchart.value?.remove(item.code, true)
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
    await makeItemContext(row)
    await drawItemContext()
  } else {
    clearItemContext(row)
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
