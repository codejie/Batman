<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { apiGetHistoryData } from '@/api/data'
import {
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElButton,
  ElTable,
  ElTableColumn
} from 'element-plus'
import SplitChart from '@/components/Chart/SplitChart.vue'
import type { SeriesDataItem } from '@/components/Chart/types'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  stock: {
    type: Object,
    required: true
  },
  result: {
    type: Object,
    required: true
  },
  dataPeriodStart: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:visible'])

const xAxisData = ref<string[]>([])
const chartSeries = ref<{ name: string; series: SeriesDataItem[] }[]>([])

const title = computed(() => {
  if (!props.stock) return ''
  return `${props.stock.name}(${props.stock.code})`
})

const form = ref({
  capital: 100000,
  buyPriceStrategy: '',
  buyQuantityStrategy: '',
  buyTimingStrategy: '',
  sellPriceStrategy: '',
  sellQuantityStrategy: '',
  sellTimingStrategy: ''
})

const tableData = ref([])
const totalAmount = computed(() => {
  return form.value.capital + tableData.value.reduce((sum, item) => sum + item.fee, 0)
})

const onExecute = () => {
  // todo
}

const handleClose = () => {
  emit('update:visible', false)
}

const calculateMA = (dayCount: number, data: any[]) => {
  var result = [];
  for (var i = 0, len = data.length; i < len; i++) {
    if (i < dayCount) {
      result.push('-');
      continue;
    }
    var sum = 0;
    for (var j = 0; j < dayCount; j++) {
      sum += data[i - j].收盘;
    }
    result.push(sum / dayCount);
  }
  return result;
}

watch(() => props.visible, (val) => {
  if (val) {
    apiGetHistoryData({ code: props.stock.code, type: props.stock.type, start: props.dataPeriodStart }).then(res => {
      if (res.result) {
        const history = res.result
        xAxisData.value = history.map((item: any) => item.日期)
        const klineData = history.map((item: any) => [item.开盘, item.收盘, item.最低, item.最高])
        const volumeData = history.map((item: any) => ({
          value: item.成交量,
          itemStyle: {
            color: item.开盘 > item.收盘 ? '#14b143' : '#ef232a'
          }
        }))

        const klineSeries = [
          { name: 'K-Line', type: 'candlestick', data: klineData },
          { name: 'MA5', type: 'line', data: calculateMA(5, history) },
          { name: 'MA10', type: 'line', data: calculateMA(10, history) },
          { name: 'MA15', type: 'line', data: calculateMA(15, history) },
        ]

        const volumeSeries = [
          { name: 'Volume', type: 'bar', data: volumeData }
        ]

        chartSeries.value = [
          { name: 'Price', series: klineSeries },
          { name: 'Volume', series: volumeSeries }
        ]
      }
    })
  }
})

</script>

<template>
  <el-dialog
    :title="title"
    :model-value="visible"
    width="80%"
    @close="handleClose"
  >
    <div class="dialog-content">
      <div class="chart-section" style="display: flex; justify-content: center;">
        <SplitChart :xAxisData="xAxisData" :series="chartSeries" height="400px" :showLegend="false" :showZoomSlider="false" />
      </div>
      <div class="form-section">
        <div class="form-panel">
          <el-form :model="form" label-width="120px">
            <el-form-item label="Capital">
              <el-input v-model="form.capital" />
            </el-form-item>
            <el-form-item label="Buy Price Strategy">
              <el-select v-model="form.buyPriceStrategy" placeholder="please select">
                <el-option label="Strategy 1" value="s1"></el-option>
                <el-option label="Strategy 2" value="s2"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Buy Quantity Strategy">
              <el-select v-model="form.buyQuantityStrategy" placeholder="please select">
                <el-option label="Strategy 1" value="s1"></el-option>
                <el-option label="Strategy 2" value="s2"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Buy Timing Strategy">
              <el-select v-model="form.buyTimingStrategy" placeholder="please select">
                <el-option label="Strategy 1" value="s1"></el-option>
                <el-option label="Strategy 2" value="s2"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Sell Price Strategy">
              <el-select v-model="form.sellPriceStrategy" placeholder="please select">
                <el-option label="Strategy 1" value="s1"></el-option>
                <el-option label="Strategy 2" value="s2"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Sell Quantity Strategy">
              <el-select v-model="form.sellQuantityStrategy" placeholder="please select">
                <el-option label="Strategy 1" value="s1"></el-option>
                <el-option label="Strategy 2" value="s2"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Sell Timing Strategy">
              <el-select v-model="form.sellTimingStrategy" placeholder="please select">
                <el-option label="Strategy 1" value="s1"></el-option>
                <el-option label="Strategy 2" value="s2"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onExecute">Execute</el-button>
            </el-form-item>
          </el-form>
        </div>
        <div class="table-panel">
          <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="index" label="Index" />
            <el-table-column prop="date" label="Date" />
            <el-table-column prop="action" label="Action" />
            <el-table-column prop="price" label="Price" />
            <el-table-column prop="quantity" label="Quantity" />
            <el-table-column prop="fee" label="Fee" />
          </el-table>
          <div class="statistics">
            Statistics: {{ totalAmount }}
          </div>
        </div>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Confirm</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
.dialog-content {
  display: flex;
  flex-direction: column;
}
.chart-section {
  margin-bottom: 20px;
}
.form-section {
  display: flex;
}
.form-panel {
  width: 50%;
  padding-right: 20px;
}
.table-panel {
  width: 50%;
}
.statistics {
  margin-top: 10px;
  text-align: right;
}
</style>