<script setup lang="ts">
import { computed } from 'vue'
import type { PropType } from 'vue'
import { ElTable, ElTableColumn } from 'element-plus'
import { AlgorithmCategoryDefinitions, AlgorithmTypeDefinitions } from '@/api/calc/defines'
import type { AggregatedReport } from './CalcReport.vue'

const props = defineProps({
  data: {
    type: Object as PropType<AggregatedReport>,
    required: true
  }
})

const getCategoryTitle = (category: number) => {
  return AlgorithmCategoryDefinitions[category]?.title || category
}

const getTypeTitle = (type: number) => {
  return AlgorithmTypeDefinitions[type]?.title || type
}

const getTableData = (report: any) => {
  if (!report) return []
  if (Array.isArray(report)) {
    return report
  }
  if (typeof report === 'object') {
    return Object.entries(report).map(([key, value]) => ({ key, value }))
  }
  return []
}

const isObjectReport = (report: any) => {
  return typeof report === 'object' && !Array.isArray(report)
}
</script>

<template>
  <div class="report-item-container">
    <p class="title">{{ props.data.stock.name }} ({{ props.data.stock.code }})</p>

    <div
      v-for="(reportInfo, index) in props.data.reports"
      :key="index"
      class="single-report-block"
    >
      <p class="subtitle">{{ getCategoryTitle(reportInfo.category) }}: {{ getTypeTitle(reportInfo.type) }}</p>

      <el-table :data="getTableData(reportInfo.report)" :border="true" size="small" stripe>
        <template v-if="isObjectReport(reportInfo.report)">
          <el-table-column prop="key" label="Property" />
          <el-table-column prop="value" label="Value" />
        </template>
        <template v-else>
          <el-table-column prop="index" label="日期" />
          <el-table-column prop="price" label="价格" />
          <el-table-column prop="trend" label="趋势信号">
            <template #default="{ row }">
              <span v-if="row.trend === 1" style="color: red">上涨</span>
              <span v-else-if="row.trend === -1" style="color: green">下跌</span>
              <span v-else-if="row.trend === 0" style="color: grey">中性</span>
            </template>
          </el-table-column>
        </template>
      </el-table>
    </div>
  </div>
</template>

<style scoped>
.report-item-container {
  margin-bottom: 16px;
}

.title {
  font-size: 1rem;
  font-weight: bold;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 1rem;
  color: #606266;
  margin: 8px 0;
}

.el-table {
  width: 100%;
}

.single-report-block {
  margin-top: 1rem;
  border: 1px solid #ebeef5;
  padding: 1rem;
  border-radius: 4px;
}
</style>
