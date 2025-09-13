<script setup lang="ts">
import { computed, PropType } from 'vue'
import { ElDialog, ElButton } from 'element-plus'
import { SplitChart } from '.'
import type { SeriesDataItem } from './types'

const props = defineProps({
  // v-model
  modelValue: {
    type: Boolean,
    required: true
  },
  // Props for SplitChart
  topSeriesData: {
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
    default: '60vh'
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
  bottomYAxisName: {
    type: String,
    default: ''
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
  <el-dialog v-model="dialogVisible" :title="props.title" width="85%" top="5vh">
    <SplitChart
      :top-series-data="props.topSeriesData"
      :bottom-series-data="props.bottomSeriesData"
      :x-axis-data="props.xAxisData"
      :height="props.height"
      :show-legend="props.showLegend"
      :x-axis-name="props.xAxisName"
      :top-y-axis-name="props.topYAxisName"
      :bottom-y-axis-name="props.bottomYAxisName"
    />
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false"> 确定 </el-button>
      </span>
    </template>
  </el-dialog>
</template>
