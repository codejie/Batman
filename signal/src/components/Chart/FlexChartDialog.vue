<script setup lang="ts">
import { computed, PropType } from 'vue'
import { ElDialog, ElButton } from 'element-plus'
// 从目录索引导入，而不是直接从 .vue 文件导入
import { FlexChart, type SeriesDataItem } from '.'

const props = defineProps({
  // v-model for dialog visibility
  modelValue: {
    type: Boolean,
    required: true,
    default: false
  },
  // Props for the FlexChart component
  seriesData: {
    type: Array as PropType<SeriesDataItem[]>,
    required: true
  },
  xAxisData: {
    type: Array as PropType<string[]>,
    required: true
  },
  title: {
    type: String,
    default: '图表'
  },
  height: {
    type: String,
    default: '50vh' // A sensible default height for a dialog
  },
  xAxisName: {
    type: String,
    default: ''
  },
  yAxisName: {
    type: String,
    default: ''
  },
  showLegend: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue'])

// Use a computed property to handle v-model binding with el-dialog
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => {
    emit('update:modelValue', val)
  }
})
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="props.title"
    width="80%"
    top="5vh"
  >
    <FlexChart
      :series-data="props.seriesData"
      :x-axis-data="props.xAxisData"
      :height="props.height"
      :x-axis-name="props.xAxisName"
      :y-axis-name="props.yAxisName"
      :show-legend="props.showLegend"
    />
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>
