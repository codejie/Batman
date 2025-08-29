<script setup lang="ts">
import { computed, ref } from 'vue'
import type { PropType } from 'vue'
import { ElTable, ElTableColumn } from 'element-plus'
import { AlgorithmCategoryDefinitions, AlgorithmTypeDefinitions } from '@/api/calc/defines'
import type { AggregatedReport } from './CalcReport.vue'
import { KLineDialog } from '@/components/KLine'

const props = defineProps({
  data: {
    type: Object as PropType<AggregatedReport>,
    required: true
  }
})

const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<any>({})

const getCategoryTitle = (category: string) => {
  return AlgorithmCategoryDefinitions[category]?.title || category
}

const getTypeTitle = (category: string, type: string) => {
  return AlgorithmTypeDefinitions[category]?.[type]?.title || type
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

function onTitleClick() {
  reqParam.value = {
    code: props.data.stock.code,
    name: props.data.stock.name,
    type: props.data.stock.type,
  }
  klineDialogVisible.value = true
}
</script>

<template>
  <div class="report-item-container">
    <p class="title" @click="onTitleClick">{{ props.data.stock.name }} ({{ props.data.stock.code }})</p>

    <div
      v-for="(reportInfo, index) in props.data.reports"
      :key="index"
      class="single-report-block"
    >
      <p class="subtitle">{{ getCategoryTitle(reportInfo.category) }}: {{ getTypeTitle(reportInfo.category, reportInfo.type) }}</p>

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
              <span v-else-if="row.trend === 0" style="color: grey">--</span>
            </template>
          </el-table-column>
        </template>
      </el-table>
    </div>
    <KLineDialog :visible="klineDialogVisible" :req-param="reqParam" @update:on-close="klineDialogVisible = false" width="60%" />
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
  cursor: pointer;
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