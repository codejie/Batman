<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn, ElDropdown, ElDropdownMenu, 
  ElDropdownItem, ElInput, ElText, ElMessage, ElRadioGroup, ElRadioButton, ElCheckboxGroup, ElCheckboxButton,
  ElDivider } from 'element-plus'
import { KLineChart4 } from '@/components/KLine'
import { onMounted, ref, watch } from 'vue';
import { calcMAData, fitKLineData, fitMACDData, fitMAData, fitVolumeData, KLineChartData,
   KLineData, MACDData, MADataGroup, makeKLineChartData, makeMACDData, makeMADataGroup, VolumeData, XData } from '@/utils/kline';
import { apiMACD } from '@/api/libs/talib';
import { formatToDate } from '@/utils/dateUtil';
import { apiCreate } from '@/api/customized';
import { apiHistory, apiInfo, HistoryDataModel } from '@/api/data/wrap';

type ItemCode = {
  type: number
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
const codeList = ref<ItemCode[]>([{ type: 1, code: '000001', name: 'A'}, { type: 1, code: '000009', name: 'b'}])
const inputCode = ref<string>()
const itemFetched = ref<boolean>(false)
const itemTitleOutput = ref<string>()
const itemDataOutput = ref<string>()

const startGroup: string[] = ['两年', '一年', '半年']
const startRange = ref<string>('半年')
const maGroup: number[] = [5, 9, 10, 12, 22, 26, 30, 45, 60]
const maSelected = ref<number[]>([5])
const secondGroup: string[] = ['Volume', 'MACD']
const secondSelected = ref<string>('Volume')
const chartModeGroup: string[] = ['KLine', 'Zoom', 'Fit']
const chartModeSelected = ref<string[]>(['KLine'])

let itemCode: ItemCode | null = null
let baseItem: ItemContext | null = null
let moreItems: ItemContext[] = []

let k_start: string = makeStart()
let k_zoom: boolean = false
let k_line: boolean = true
let k_fit: boolean = false

let searchTimer: NodeJS.Timeout
watch(
  () => inputCode.value,
  async () => {
    if (!inputCode.value || inputCode.value.length < 6)
      return

    clearTimeout(searchTimer)
    searchTimer = setTimeout(async () => {
      await fetchItemCode(inputCode.value!)
    }, 300)
  }
)

onMounted(() => {
  setGrid(kchart.value)
  if (props.code) {
    inputCode.value = props.code
  }
})

function setGrid(chart) {
  chart.reset()
  if (k_zoom) {
    chart?.addGrid(0, '4%', '4%', '4%', '10%')
  } else {
    chart?.addGrid(0, '4%', '4%', '4%', '40%')
    chart?.addGrid(1, '4%', '70%', '4%', '6%')
  }
}

function setAxis(chart, data: XData) {
  if (k_zoom) {
    chart.addAxis(0, data, true)
    chart.addAxisPointer([0])
  } else {
    chart.addAxis(0, data, true)
    chart.addAxis(1, data, false)
    chart.addAxisPointer([0, 1])
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
    const fitData = k_fit ? fitKLineData(data, base) : data
    console.log(`fitData = ${fitData}`)
    chart.addKLine(0, name, fitData.data, false, true)
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
    chart.addBar(1, name, fitData.data)
  }
}

function setMACD(item: ItemCode, chart, data: MACDData) {
  chart.addLine(1, item.code + '-DIF', data.dif)
  chart.addLine(1, item.code + '-DEA', data.dea)
  chart.addBar(1, item.code + '-DIFF', data.macd) 
}

function addMACD(item: ItemCode, chart, data: MACDData, base: MACDData) {
  const fitData = k_fit ? fitMACDData(data, base) : data
  chart.addLine(1, item.code + '-DIF', fitData.dif)
  chart.addLine(1, item.code + '-DEA', fitData.dea)
  chart.addBar(1, item.code + '-DIFF', fitData.macd) 
}

function setMAData(item: ItemCode, chart, data: MADataGroup) {
  for (const key of Object.keys(data)) {
    const name = item.code + '-MA' + key
    chart.addLine(0, name, data[key].data)
  }
}

function addMAData(item: ItemCode, chart, data: MADataGroup, base: MADataGroup) {
  for (const key of Object.keys(data)) {
    console.log(`k_fit = ${k_fit}`)
    const fitData = k_fit ? fitMAData(data[key], base[key]) : data[key]
    const name = item.code + '-MA' + key
    chart.addLine(0, name, fitData.data)
  }
}

async function fetchItemCode(code: string) {
  itemTitleOutput.value = undefined
  itemDataOutput.value = undefined
  itemFetched.value = false
  
  const ret = await apiInfo(
    {
      code: code
    },
    (codeType.value == 'Stock' ? 1 : 0)
)
  if (ret.result) {
    itemFetched.value = true
    itemCode = {
      type: codeType.value == 'Stock' ? 1 : 0,
      code: ret.result.code,
      name: ret.result.name
    }
    itemTitleOutput.value = `${itemCode.code}(${itemCode.name}):  `
    const hret = await apiHistory(
      {
        code: itemCode.code
      },
      (codeType.value == 'Stock' ? 1 : 0)
    )
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

function  makeStart(): string {
  const date: Date = new Date()
  switch(startRange.value) {
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
  return formatToDate(date)
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

function checkItemContext(item: ItemCode): boolean {
  if (baseItem && (baseItem.item.code == item.code && baseItem.item.type == item.type))
    return true
  for (let i = 0; i < moreItems.length; ++ i) {
    if (moreItems[i].item.code == item.code && moreItems[i].item.type == item.type)
      return true
  }
  return false
}

function makeItemContext(item: ItemCode): Promise<ItemContext> {
  return new Promise<ItemContext>((resolve) => {
    apiHistory(
      {
        code: item.code,
        start: k_start
      },
      item.type
  ).then(ret => {
      const historyData = ret.result
      const context: ItemContext = {
        item: item,
        historyData: historyData,
        chartData: makeKLineChartData(historyData)    
      }
      makeItemContextMAData(maSelected.value, context)
      resolve(context)    
    })
  })
}

async function createItemContext(item: ItemCode) {
  if (checkItemContext(item)) return
  const context = await makeItemContext(item)
  if (baseItem) {
    moreItems.push(context)
  } else {
    baseItem = context
  }
}

async function refreshItemContextData() {
  if (baseItem) {
    baseItem = await makeItemContext(baseItem.item)

    for (let index = 0; index < moreItems.length; ++ index) {
      moreItems[index] = await makeItemContext(moreItems[index].item)
    }
  }
  await drawItemContexts()
}

function makeItemContextMAData(maSelected: number[], context: ItemContext) {
  context.chartData.maData = {}
  maSelected.forEach(item => {
    context.chartData.maData![item] = calcMAData(item, context.chartData.xData, context.chartData.klineData)
  })
}

function refreshItemContextMAData() {
  clearChartSeries('-MA', kchart.value)
  if (baseItem) {
    makeItemContextMAData(maSelected.value, baseItem)
    setMAData(baseItem.item, kchart.value, baseItem.chartData.maData!)
    for (let index = 0; index < moreItems.length; ++ index) {
      makeItemContextMAData(maSelected.value, moreItems[index])
      addMAData(moreItems[index].item, kchart.value, moreItems[index].chartData.maData!, baseItem!.chartData.maData!)
    }
  }
}

async function refreshItemContextVolumnData() {
  if (!baseItem) return

  clearChartSeries('-V', kchart.value)  
  clearChartSeries('-DIF', kchart.value)
  clearChartSeries('-DEA', kchart.value)
  clearChartSeries('-DIFF', kchart.value)

  if (secondSelected.value == 'Volume') {
    setVolume(baseItem.item, kchart.value, baseItem.chartData.volumeData)
  } else {
    if (!baseItem.chartData.macdData) {
      baseItem.chartData.macdData = await fetchItemMACDData(baseItem.chartData.xData, baseItem.chartData.klineData)
    }
    setMACD(baseItem.item, kchart.value, baseItem.chartData.macdData)
  }

  for (let index = 0; index < moreItems.length; ++ index) {
    const item = moreItems[index]
    if (secondSelected.value == 'Volume') {
      addVolume(item.item, kchart.value, item.chartData.volumeData, baseItem!.chartData.volumeData)
    } else {
      if (!item.chartData.macdData) {
        item.chartData.macdData = await fetchItemMACDData(item.chartData.xData, item.chartData.klineData)
      }
      addMACD(item.item, kchart.value, item.chartData.macdData, baseItem!.chartData.macdData!)      
    }    
  }  
}

async function drawItemContexts() {
  itemTitleOutput.value = undefined
  itemDataOutput.value = undefined
  setGrid(kchart.value)

  await drawBaseItem()
  await drawMoreItems()
}

async function drawBaseItem() {
  if (!baseItem) {
    return
  }
  itemTitleOutput.value = `${baseItem.item.code}(${baseItem.item.name}):  `
  itemDataOutput.value = makeItemDataOutput(baseItem.historyData[baseItem.historyData.length - 1])

  // setGrid(kchart.value)
  setAxis(kchart.value, baseItem.chartData.xData)
  setKLine(baseItem.item, kchart.value, baseItem.chartData.klineData)
  if (!baseItem.chartData.maData) {
    baseItem.chartData.maData = makeMADataGroup(maSelected.value, baseItem.chartData)
  }
  setMAData(baseItem.item, kchart.value, baseItem.chartData.maData)
  if (!k_zoom) {
    if (secondSelected.value == 'Volume') {
      setVolume(baseItem.item, kchart.value, baseItem.chartData.volumeData)
    } else {
      if (!baseItem.chartData.macdData) {
        baseItem.chartData.macdData = await fetchItemMACDData(baseItem.chartData.xData, baseItem.chartData.klineData)
      }
      setMACD(baseItem.item, kchart.value, baseItem.chartData.macdData)
    }
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
    if (!k_zoom) {
      if (secondSelected.value == 'Volume') {
        addVolume(item.item, kchart.value, item.chartData.volumeData, baseItem!.chartData.volumeData)
      } else {
        if (!item.chartData.macdData) {
          item.chartData.macdData = await fetchItemMACDData(item.chartData.xData, item.chartData.klineData)
        }
        addMACD(item.item, kchart.value, item.chartData.macdData, baseItem!.chartData.macdData!)      
      }
    }
  }
}

function redrawItemContextKLineData() {
  if (baseItem) {
    setKLine(baseItem.item, kchart.value, baseItem.chartData.klineData)
    for (let index = 0; index < moreItems.length; ++ index) {
      const item = moreItems[index]
      addKLine(item.item, kchart.value, item.chartData.klineData, baseItem!.chartData.klineData!)
    } 
  }
}

function clearItemContext(item: ItemCode) {
  if (item == baseItem?.item) {
    if (moreItems.length > 0) {
      baseItem = moreItems[0]
      moreItems = moreItems.slice(1)
    } else {
      baseItem = null
    }
  } else {
    moreItems = moreItems.filter(element => element.item != item)
  }
}

function clearChartSeries(key: string, chart) {
  chart.remove(key, true)
}

async function onCodeTypeCommand(cmd: string) {
  codeType.value = cmd
  if (!inputCode.value || inputCode.value.length < 6)
    return
  await fetchItemCode(inputCode.value)
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
  const added: boolean = selected.includes(row)
  if (added) {
    await createItemContext(row) // makeItemContext(row)
    // await drawItemContexts()    
  } else {
    clearItemContext(row)
    // clearChartSeries(row.code, kchart.value)
  }
  await drawItemContexts()
}

async function onStartChanged() {
  k_start = makeStart()
  await refreshItemContextData()
}

function onMaGroupChanged() {
  refreshItemContextMAData()
}

async function onSecondChanged() {
  await refreshItemContextVolumnData()
}

async function onChartModeChanged() {
  console.log(`chartmode = ${chartModeSelected.value}`)
  const kline = chartModeSelected.value.includes('KLine')
  if (k_line != kline) {
    k_line = kline
    redrawItemContextKLineData()
  }
  const zoom = chartModeSelected.value.includes('Zoom')
  if (k_zoom != zoom) {
    k_zoom = zoom
    console.log(`kzoom = ${k_zoom}`)
    await drawItemContexts()
  }
  const fit = chartModeSelected.value.includes('Fit')
  if (k_fit != fit) {
    k_fit = fit
    await drawItemContexts()
  }
}

async function onCustomizedClick() {
  const { type, code } = baseItem ? baseItem.item : itemCode!
  const ret = await apiCreate({
    code: code,
    type: type
  })
  if (ret.code == 0) {
    ElMessage({
        type: 'success',
        message: `${code} added to customized list.`
      })    
  }
}

</script>
<template>
  <ContentWrap title="Lookup">
    <ElRow :gutter="24">
      <ElCol :span="24">
        <ElDropdown trigger="click" style="padding-right: 8px;" @command="onCodeTypeCommand">
          <ElButton size="default">{{ codeType }}</ElButton>
          <template #dropdown>
            <ElDropdownMenu>
              <ElDropdownItem command="Stock">Stock</ElDropdownItem>
              <ElDropdownItem command="Index">Index</ElDropdownItem>
            </ElDropdownMenu>
          </template>
        </ElDropdown>
        <ElInput v-model="inputCode" size="default" type="string" :clearable="true" style="width: 100px; padding-right: 8px;" maxlength="6" />
        <ElButton type="primary" size="default" :disabled="!itemFetched" @click="onItemAddClick">+</ElButton>
        <ElText tag="b" size="large" style="padding-left: 16px; text-align: center; height: 100%;" >{{ itemTitleOutput }}  {{ itemDataOutput }}</ElText>
      </ElCol>
    </ElRow>
    <ElDivider border-style="dashed" />    
    <ElRow :gutter="24">
      <ElCol :span="3">
        <ElTable :data="codeList" size="small" @select="onCodeListSelected" :border="true" max-height="auto">
          <ElTableColumn type="selection" width="30" />
          <ElTableColumn prop="code" label="Code" />
          <ElTableColumn prop="name" label="Name" />
        </ElTable>
      </ElCol>
      <ElCol :span="21">
        <ElRow :gutter="24">
          <ElCol :span="4">
            <ElRadioGroup v-model="startRange" size="small" style="float: left;" @change="onStartChanged">
              <ElRadioButton v-for="item in startGroup" :key="item" :value="item" :label="item" />
            </ElRadioGroup>
          </ElCol>
          <ElCol :span="7">
            <ElCheckboxGroup v-model="maSelected" size="small" style="display: flex; justify-content: center;" @change="onMaGroupChanged">
              <ElCheckboxButton v-for="item in maGroup" :key="item" :value="item" :label="item" :checked="item in maSelected" />
            </ElCheckboxGroup>
          </ElCol>
          <ElCol :span="4">
            <ElRadioGroup v-model="secondSelected" size="small" :disabled="chartModeSelected.includes('Zoom')" style="display: flex; justify-content: center;" @change="onSecondChanged">
              <ElRadioButton v-for="item in secondGroup" :key="item" :value="item" :label="item" />
            </ElRadioGroup>
          </ElCol>
          <ElCol :span="3">
            <ElCheckboxGroup v-model="chartModeSelected" size="small" style="display: flex; justify-content: center;" @change="onChartModeChanged">
              <ElCheckboxButton v-for="item in chartModeGroup" :key="item" :value="item" :label="item" :checked="item in chartModeSelected" />
            </ElCheckboxGroup>
          </ElCol>
          <ElCol :span="6">
            <ElButton size="small" style="float: right;" :disabled="itemTitleOutput==undefined" @click="onCustomizedClick">自</ElButton>
          </ElCol>
        </ElRow>
        <KLineChart4 ref="kchart" />
      </ElCol>
    </ElRow>
  </ContentWrap>
</template>
<style lang="css">
.row {
  padding: 4px;
  outline: 1px solid gray;
}
.col {
  outline: 1px solid red;
}
.text {
  width: 100%;
  height: 100%;
  border: 1px solid green;
}
</style>
