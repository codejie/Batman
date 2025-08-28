<script setup lang="ts">
import { computed } from 'vue'
import { ElDescriptions, ElDescriptionsItem } from 'element-plus'
import type { AlgorithmItem } from '@/api/calc'
import {
  AlgorithmStockListDefinitions,
  AlgorithmDataPeriodDefinitions,
  AlgorithmReportPeriodDefinitions
} from '@/api/calc/defines'

const props = defineProps<{
  item: AlgorithmItem | null
}>()

const listTypeText = computed(() => {
  if (props.item === null) return ''
  return AlgorithmStockListDefinitions[props.item.list_type] || '未知'
})

const dataPeriodText = computed(() => {
  if (props.item === null) return ''
  return AlgorithmDataPeriodDefinitions[props.item.data_period] || '未知'
})

const reportPeriodText = computed(() => {
  if (props.item === null) return ''
  return AlgorithmReportPeriodDefinitions[props.item.report_period] || '未知'
})
</script>

<template>
  <div v-if="item" class="calc-item-details">
    <p class="detail-title">计算详情</p>
    <el-descriptions :column="3" :border="true" label-width="160">
      <el-descriptions-item label="名称">{{ item.name }}</el-descriptions-item>
      <el-descriptions-item label="备注" :span="2">{{ item.remarks }}</el-descriptions-item>
      <el-descriptions-item label="列表类型">{{ listTypeText }}</el-descriptions-item>
      <el-descriptions-item label="数据期间">{{ dataPeriodText }}</el-descriptions-item>
      <el-descriptions-item label="报告期间">{{ reportPeriodText }}</el-descriptions-item>
    </el-descriptions>
  </div>
</template>

<style scoped>
.calc-item-details {
  margin-bottom: 20px;
}
.detail-title {
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 600;
}
</style>
