<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn, ElDropdown, ElDropdownMenu, 
  ElDropdownItem, ElInput, ElText, ElMessage, ElRadioGroup, ElRadioButton } from 'element-plus'
import { KLineChart4 } from '@/components/KLine'
import { onMounted, ref, watch } from 'vue';
import { apiHistory, apiInfo } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { calcMAData, fitKLineData, fitMACDData, fitMAData, fitVolumeData, KLineChartData,
   KLineData, MACDData, MADataGroup, makeKLineChartData, makeMACDData, makeMADataGroup, VolumeData, XData } from '@/utils/kline';
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
const maSelected = ref<number[]>([5])
const secondMode = ref<string>('MACD')
const fitMode = ref<boolean>(true)

const startGroup: string[] = ['两年', '一年', '半年']
let startRange: string

let itemCode: ItemCode | null = null
let baseItem: ItemContext | null = null
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
    chart.addKLine(0, name, data.data, true, true)
  } else {
    chart.remove(name)
  }
}

function addKLine(item: ItemCode, chart, data: KLineData, base: KLineData) {
  const name = item.code + '-K'
  if (k_line) {
    const fitData = fitMode.value ? fitKLineData(data, base) : data
    chart.addKLine(0, item.code + '-K', fitData.data, true, true)
  } else {
    chart.remove(name)
  }
}

function setVolume(item: ItemCode, chart, data: VolumeData) {
  if (!k_zoom) {
    const name = item.code + '-V'
    chart.addBar(1, name, data.data)
  }
}

function addVolume(item: ItemCode, chart, data: VolumeData, base: VolumeData) {
  if (!k_zoom) {
    const fitData = fitVolumeData(data, base)
    const name = item.code + '-V'
    chart.addBar(1, name, fitData)
  }
}

function setMACD(item: ItemCode, chart, data: MACDData) {
  chart.addLine(1, item.code + '-DIF', data.dif)
  chart.addLine(1, item.code + '-DEA', data.dea)
  chart.addBar(1, item.code + '-MACD', data.macd) 
}

function addMACD(item: ItemCode, chart, data: MACDData, base: MACDData) {
  const fitData = fitMode.value ? fitMACDData(data, base) : data
  chart.addLine(1, item.code + '-DIF', fitData.dif)
  chart.addLine(1, item.code + '-DEA', fitData.dea)
  chart.addBar(1, item.code + '-MACD', fitData.macd) 
}

function setMAData(item: ItemCode, chart, data: MADataGroup) {
  for (const key of Object.keys(data)) {
    const name = item.code + '-' + key
    chart.addLine(0, name, data[key].data)
  }
}

function addMAData(item: ItemCode, chart, data: MADataGroup, base: MADataGroup) {
  for (const key of Object.keys(data)) {
    const fitData = fitMode.value ? fitMAData(data[key], base[key]) : data
    // console.log(fitData)
    const name = item.code + '-' + key
    chart.addLine(0, name, fitData)
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

async function fetchItemMACDData( xData: XData, klineData: KLineData): Promise<MACDData> {
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
    context.chartData.maData![item] = calcMAData(item, context.chartData.xData, context.chartData.klineData)
  })
}

async function drawItemContexts() {
  await drawBaseItem()
  await drawMoreItems()
}

async function drawBaseItem() {
  const context = baseItem!
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
      context.chartData.macdData = await fetchItemMACDData(context.chartData.xData, context.chartData.klineData)
    }
    setMACD(context.item, kchart.value, context.chartData.macdData)
  }
}

async function drawMoreItems() {
  for (let i = 0;i < moreItems.length; ++ i) {
    const item = moreItems[i]
    addKLine(item.item, kchart.value, item.chartData.klineData, baseItem!.chartData.klineData)
    if (!item.chartData.maData) {
      item.chartData.maData = makeMADataGroup(maSelected.value, item.chartData)
    }
    addMAData(item.item, kchart.value, item.chartData.maData, baseItem!.chartData.maData!)
    if (secondMode.value == 'Volume') {
      addVolume(item.item, kchart.value, item.chartData.volumeData, baseItem!.chartData.volumeData)
    } else {
      if (!item.chartData.macdData) {
        item.chartData.macdData = await fetchItemMACDData(item.chartData.xData, item.chartData.klineData)
      }
      addMACD(item.item, kchart.value, item.chartData.macdData, baseItem!.chartData.macdData!)      
    }
  }
}

function clearItemContext(item: ItemCode): boolean {
  let changed = false
  if (item == baseItem?.item) {
    if (moreItems.length > 0) {
      baseItem = moreItems[0]
      moreItems = moreItems.slice(1)

      changed = true
    } else {
      baseItem = null
    }
  } else {
    moreItems = moreItems.filter(element => element.item != item)
  }
  return changed
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

async function onCodeListSelected(selected: ItemCode[], row: ItemCode) {
  console.log(selected)
  console.log(row)

  const added: boolean = selected.includes(row)
  if (added) {
    await makeItemContext(row)
    await drawItemContexts()    
  } else {
    if (clearItemContext(row)) {
      await drawItemContexts()
    } else {
      kchart.value?.remove(row.code, true)
    }
  }

  // if (selected.includes(row)) {
  //   await makeItemContext(row)
  //   await drawItemContexts()
  // } else {
  //   clearItemContext(row)
  // }
}

async function onStartChanged() {
  const date: Date = new Date()
  switch(startRange) {
    case '两年':
      date.setFullYear(date.getFullYear() - 2)
      break
    case '半年':
      date.setMonth(date.getMonth() - 6)
      break
    case '一年':
    default:
      date.setFullYear(date.getFullYear() - 1)
  }
  // props.reqParam!.start = date.toISOString().slice(0, 10)

  // await fetchHistoryData()
  // updateChartOptions(historyData)
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
        <ElTable :data="codeList" size="small" @select="onCodeListSelected" :border="true" max-height="auto" highlight-current-row>
          <ElTableColumn type="selection" width="30" />
          <ElTableColumn prop="code" label="Code" />
          <ElTableColumn prop="name" label="Name" />
          <!-- <ElTableColumn label="Action" /> -->
        </ElTable>
      </ElCol>
      <ElCol :span="21">
        <ElRow class="row" :gutter="24">
          <ElCol :span="5">
            <ElRadioGroup v-model="startRange" size="small" style="float: right;" @change="onStartChanged">
              <ElRadioButton v-for="item in startGroup" :key="item" :value="item" :label="item" />
            </ElRadioGroup>
          </ElCol>
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
