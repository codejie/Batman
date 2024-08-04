<script setup lang="ts">
import { computed, onMounted, PropType, ref, unref, watch } from 'vue';
import { ElRow, ElCol, ElButton, ElCheckboxGroup, ElCheckboxButton, ElRadioGroup, ElRadioButton, ElMessage, ElTable, ElTableColumn } from 'element-plus';
import { ReqParam, ShowParam } from '..';
import { apiCreate } from '@/api/customized';
import KLineChart from './KLineChart.vue';

const props = defineProps({
  param: {
    type: Object as PropType<ReqParam>,
    required: true
  },
  showTable: {
    type: Boolean,
    required: false,
    default: () => false
  }
})
const startGroup: string[] = ['两年', '一年', '半年']
const maGroup: number[] = [5, 7, 9, 12, 17, 22, 26, 30, 45, 60]
const klineGroup: string[] = ['KLine', 'Zoom']
let start: string = '2023-01-01'
let zoom: boolean = false
let kline: boolean = true

const title = ref<string>('')
const startRange = ref<string>('一年')
const maLines = ref<number[]>([7, 9, 12])
const zoom_kline = ref<string[]>(['KLine'])

const showParam = ref<ShowParam>({
  maLines: maLines.value,
  hideVolume: zoom,
  markLines: true,
  hideKLine: !kline  
})
const reqParam = ref<ReqParam>()

function updateDataParam(code: string) {
  reqParam.value = {
    code: code,
    start: start
  }
}

function updateShowParam() {
  showParam.value = {
    maLines: maLines.value,
    hideVolume: zoom,
    markLines: true,
    hideKLine: !kline      
  }
}

function updateTitle() {
  title.value = `${props.param.code}(${props.param.name})`
}

watch(
  () => props.param,
  () => {
    updateDataParam(props.param.code)
    updateTitle()
})

onMounted(() =>{
  const date: Date = new Date()
  date.setFullYear(date.getFullYear() - 1)
  start = date.toISOString().slice(0, 10)

  updateDataParam(props.param.code)
  updateTitle()
})

async function onCustomizedClick() {
  const ret = await apiCreate({
    code: props.param.code,
    type: 1
  })
  if (ret.code == 0) {
    ElMessage({
        type: 'success',
        message: `${props.param.code} added to customized list.`
      })    
  }
}

function onKLineChanged() {
  console.log(zoom_kline.value)
  zoom = zoom_kline.value.includes('Zoom')
  kline = zoom_kline.value.includes('KLine')
  updateShowParam()
}

function onMaGroupChanged() {
  // maLines.value = values
  // console.log(maLines.value)
  updateShowParam()
}

function onStartChanged() {
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
  start = date.toISOString().slice(0, 10)
  updateDataParam(props.param.code)
}

const kc = ref(null)
const originData = computed(() => unref(kc)?.originData.reverse())

</script>
<template>
  <ElRow :gutter="24">
    <ElCol :span="4">
      <div style="float: right;">
        <!-- {{ title }} -->
        <ElButton size="small" @click="onCustomizedClick">Add to Customized</ElButton>
      </div>
    </ElCol>
    <ElCol :span="6">
      <ElRadioGroup v-model="startRange" size="small" style="float: right;" @change="onStartChanged">
        <ElRadioButton v-for="item in startGroup" :key="item" :value="item" :label="item" />
      </ElRadioGroup>
    </ElCol>
    <ElCol :span="10">
      <ElCheckboxGroup v-model="maLines" size="small" style="float: center; margin-right: 12px;" @change="onMaGroupChanged">
        <ElCheckboxButton v-for="item in maGroup" :key="item" :value="item" :label="item" :checked="item in maLines" />
      </ElCheckboxGroup>
    </ElCol>
    <ElCol :span="4">
      <ElCheckboxGroup v-model="zoom_kline" size="small" style="float: ceneter;" @change="onKLineChanged">
        <ElCheckboxButton v-for="item in klineGroup" :key="item" :value="item" :label="item" :checked="item in zoom_kline" />
      </ElCheckboxGroup>        
    </ElCol>
  </ElRow>
  <ElRow :gutter="24" style="margin-top: 12px;">
    <KLineChart ref="kc" :reqParam="reqParam" :showParam="showParam" />
  </ElRow>
  <ElRow v-if="showTable" :utter="24">
    <ElTable :data="originData" :stripe="true" :border="true" max-height="300" style="width: 100%;">
      <ElTableColumn prop="date" label="日期" width="120" />            
      <ElTableColumn prop="price" label="现价" width="100" />
      <ElTableColumn prop="percentage" label="涨跌幅%" width="100" />
      <ElTableColumn prop="amount" label="涨跌额" width="100" />
      <ElTableColumn prop="volatility" label="振幅%" width="100" />          
      <ElTableColumn prop="open" label="今开" width="100" />
      <ElTableColumn prop="close" label="昨收" width="100" />
      <ElTableColumn prop="high" label="最高" width="100" />
      <ElTableColumn prop="low" label="最低" width="100" />
      <ElTableColumn prop="volume" label="成交量" width="120" />
      <ElTableColumn prop="turnover" label="成交额" width="140" />
      <ElTableColumn prop="rate" label="换手率%" width="100" />
    </ElTable>
  </ElRow>    
</template>
<style lang="css">
</style>
