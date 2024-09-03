<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn, ElDropdown, ElDropdownMenu, 
  ElDropdownItem, ElInput, ElText, ElMessage, ElRadioGroup, ElRadioButton, ElCheckboxGroup, ElCheckboxButton } from 'element-plus'
import { KLineChart4 } from '@/components/KLine'
import { onMounted, ref, watch } from 'vue';
import { apiHistory, apiInfo } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { calcMAData, fitKLineData, fitMACDData, fitMAData, fitVolumeData, KLineChartData,
   KLineData, MACDData, MADataGroup, makeKLineChartData, makeMACDData, makeMADataGroup, VolumeData, XData } from '@/utils/kline';
import { apiMACD } from '@/api/libs/talib';
import { formatToDate } from '@/utils/dateUtil';

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

const fitMode = ref<boolean>(true)

const startGroup: string[] = ['两年', '一年', '半年']
const startRange = ref<string>('半年')
const maGroup: number[] = [5, 9, 10, 12, 22, 26, 30, 45, 60]
const maSelected = ref<number[]>([5, 10, 22])
const secondGroup: string[] = ['Volume', 'MACD']
const secondSelected = ref<string>('Volume')
const chartModeGroup: string[] = ['KLine', 'Zoom', 'Fit']
const chartModeSelected = ref<string[]>(['KLine', 'Fit'])


let itemCode: ItemCode | null = null
let baseItem: ItemContext | null = null
let moreItems: ItemContext[] = []

let k_start: string = makeStart()
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
    }, 400)
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
  chart.addBar(1, item.code + '-DIFF', data.macd) 
}

function addMACD(item: ItemCode, chart, data: MACDData, base: MACDData) {
  const fitData = fitMode.value ? fitMACDData(data, base) : data
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
    const fitData = fitMode.value ? fitMAData(data[key], base[key]) : data
    // console.log(fitData)
    const name = item.code + '-MA' + key
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
  if (baseItem && baseItem.item.code == item.code)
    return true
  for (let i = 0; i < moreItems.length; ++ i) {
    if (moreItems[i].item.code == item.code)
      return true
  }
  return false
}

function makeItemContext(item: ItemCode): Promise<ItemContext> {
  return new Promise<ItemContext>((resolve) => {
    apiHistory({
      code: item.code,
      start: k_start
    }).then(ret => {
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
  }
  for (let index = 0; index < moreItems.length; ++ index) {
    moreItems[index] = await makeItemContext(moreItems[index].item)
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
  }
  for (let index = 0; index < moreItems.length; ++ index) {
    makeItemContextMAData(maSelected.value, moreItems[index])
    addMAData(moreItems[index].item, kchart.value, moreItems[index].chartData.maData!, baseItem!.chartData.maData!)
  }
}

async function drawItemContexts() {
  await drawBaseItem()
  await drawMoreItems()
}

async function drawBaseItem() {
  if (!baseItem) return
  itemTitleOutput.value = `${baseItem.item.code}(${baseItem.item.name}):  `
  itemDataOutput.value = makeItemDataOutput(baseItem.historyData[baseItem.historyData.length - 1])

  setGrid(kchart.value)
  setAxis(kchart.value, baseItem.chartData.xData)
  setKLine(baseItem.item, kchart.value, baseItem.chartData.klineData)
  if (!baseItem.chartData.maData) {
    baseItem.chartData.maData = makeMADataGroup(maSelected.value, baseItem.chartData)
  }
  setMAData(baseItem.item, kchart.value, baseItem.chartData.maData)
  if (secondSelected.value == 'Volume') {
    setVolume(baseItem.item, kchart.value, baseItem.chartData.volumeData)
  } else {
    if (!baseItem.chartData.macdData) {
      baseItem.chartData.macdData = await fetchItemMACDData(baseItem.chartData.xData, baseItem.chartData.klineData)
    }
    setMACD(baseItem.item, kchart.value, baseItem.chartData.macdData)
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

function clearChartSeries(key: string, chart) {
  chart.remove(key, true)
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
    await createItemContext(row) // makeItemContext(row)
    await drawItemContexts()    
  } else {
    if (clearItemContext(row)) {
      await drawItemContexts()
    } else {
      clearChartSeries(row.code, kchart.value)
    }
  }
}

async function onStartChanged() {
  k_start = makeStart()
  await refreshItemContextData()
}

function onMaGroupChanged() {
  refreshItemContextMAData()
}

function onSecondChanged() {

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
        <ElInput v-model="inputCode" style="width: 80px;" max-length="6" />
        <ElButton type="primary" :disabled="!itemFetched" @click="onItemAddClick">+</ElButton>
        <ElText tag="b" size="default">{{ itemTitleOutput }}</ElText>
        <ElText size="default">{{ itemDataOutput }}</ElText>
      </ElCol>
    </ElRow>
    <ElRow class="row" :gutter="24">
      <ElCol :span="3">
        <ElTable :data="codeList" size="small" @select="onCodeListSelected" :border="true" max-height="auto">
          <ElTableColumn type="selection" width="30" />
          <ElTableColumn prop="code" label="Code" />
          <ElTableColumn prop="name" label="Name" />
        </ElTable>
      </ElCol>
      <ElCol :span="21">
        <ElRow class="row" :gutter="24">
          <ElCol class="col" :span="4">
            <ElRadioGroup v-model="startRange" size="small" style="float: left;" @change="onStartChanged">
              <ElRadioButton v-for="item in startGroup" :key="item" :value="item" :label="item" />
            </ElRadioGroup>
          </ElCol>
          <ElCol class="col" :span="7">
            <ElCheckboxGroup v-model="maSelected" size="small" style="display: flex; justify-content: center;" @change="onMaGroupChanged">
              <ElCheckboxButton v-for="item in maGroup" :key="item" :value="item" :label="item" :checked="item in maSelected" />
            </ElCheckboxGroup>
          </ElCol>
          <ElCol class="col" :span="3">
            <ElRadioGroup v-model="secondSelected" size="small" style="display: flex; justify-content: center;" @change="onSecondChanged">
              <ElRadioButton v-for="item in secondGroup" :key="item" :value="item" :label="item" />
            </ElRadioGroup>
          </ElCol>
          <ElCol class="col" :span="3">
            <ElCheckboxGroup v-model="chartModeSelected" size="small" style="display: flex; justify-content: center;" @change="onChartModeChanged">
              <ElCheckboxButton v-for="item in chartModeGroup" :key="item" :value="item" :label="item" :checked="item in chartModeSelected" />
            </ElCheckboxGroup>
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
.col {
  outline: 1px solid red;
}
</style>
