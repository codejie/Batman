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
  return AlgorithmTypeDefinitions[category]?.types?.[type]?.title || type
}

const mergedArrayData = computed(() => {
  if (!props.data) {
    return { stock: null, reports: [] };
  }

  if (!props.data.reports || props.data.reports.length === 0) {
    return { stock: props.data.stock, reports: [] };
  }

  const reportGroups = new Map<string, any[]>();

  props.data.reports.forEach(reportInfo => {
    const key = JSON.stringify({
      category: reportInfo.category,
      type: reportInfo.type,
      arguments: reportInfo.arguments
    });

    if (!reportGroups.has(key)) {
      reportGroups.set(key, []);
    }
    reportGroups.get(key)!.push(reportInfo);
  });

  return {
    stock: props.data.stock,
    reports: Array.from(reportGroups.values()).flat()
  };
})

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

    <div v-if="mergedArrayData.reports.length > 0" class="single-report-block">
      
      <el-table :data="mergedArrayData.reports" :border="true" size="small" stripe :show-header="false" default-expand-all>
        <el-table-column type="expand">
          <template #default="{ row }">
            <div v-if="row.results && row.results.length > 0" class="mx-24px my-8px">
              <el-table :data="row.results" :border="true" size="small" stripe>
                <el-table-column prop="index" label="日期" />
                <el-table-column prop="trend" label="趋势信号">
                  <template #default="{ row: innerRow }">
                    <span v-if="innerRow.trend === 1" style="color: red">上涨</span>
                    <span v-else-if="innerRow.trend === -1" style="color: green">下跌</span>
                    <span v-else-if="innerRow.trend === 0" style="color: grey">--</span>
                  </template>
                </el-table-column>
                <el-table-column prop="price" label="价格" />
              </el-table>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="Index" width="60">
          <template #default="scope">
            <b>{{ scope.$index + 1 }}</b>
          </template>
        </el-table-column>
        <el-table-column label="Title">
          <template #default="{ row }">
            <b>
              <span>
                {{ getCategoryTitle(row.category) }}: {{ getTypeTitle(row.category, row.type) }}
                <span v-if="row.arguments">
                  [{{
                    Object.entries(row.arguments)
                      .map(([key, value]) => `${key}=${value}`)
                      .join(', ')
                  }}]
                </span>
              </span>
            </b>
          </template>
        </el-table-column>
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