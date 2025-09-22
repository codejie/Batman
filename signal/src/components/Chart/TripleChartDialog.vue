<script setup lang="ts">
import { computed, PropType } from 'vue'
import { ElDialog, ElButton } from 'element-plus'
import { TripleChart } from '.' // Changed from SplitChart
import type { SeriesDataItem } from './types'

const props = defineProps({
  // v-model
  modelValue: {
    type: Boolean,
    required: true
  },
  // Props for TripleChart
  topSeriesData: {
    type: Array as PropType<SeriesDataItem[]>,
    required: true
  },
  middleSeriesData: {
    // Added
    type: Array as PropType<SeriesDataItem[]>,
    required: true
  },
  bottomSeriesData: {
    type: Array as PropType<SeriesDataItem[]>,
    required: true
  },
  xAxisData: {
    type: Array as PropType<string[]>,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '60vh' // Adjusted height
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  xAxisName: {
    type: String,
    default: ''
  },
  topYAxisName: {
    type: String,
    default: ''
  },
  middleYAxisName: {
    // Added
    type: String,
    default: ''
  },
  bottomYAxisName: {
    type: String,
    default: ''
  },
  gridRatios: {
    // Added
    type: Array as PropType<number[]>,
    default: () => [3, 1, 2]
  }
})

const emit = defineEmits(['update:modelValue'])

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => {
    emit('update:modelValue', val)
  }
})
</script>

<template>
  <el-dialog v-model="dialogVisible" :title="props.title" width="75%" top="5vh">
    <TripleChart
      :top-series-data="props.topSeriesData"
      :middle-series-data="props.middleSeriesData"
      :bottom-series-data="props.bottomSeriesData"
      :x-axis-data="props.xAxisData"
      :height="props.height"
      :show-legend="props.showLegend"
      :x-axis-name="props.xAxisName"
      :top-y-axis-name="props.topYAxisName"
      :middle-y-axis-name="props.middleYAxisName"
      :bottom-y-axis-name="props.bottomYAxisName"
      :grid-ratios="props.gridRatios"
    />
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false"> 确定 </el-button>
      </span>
    </template>
  </el-dialog>
</template>
