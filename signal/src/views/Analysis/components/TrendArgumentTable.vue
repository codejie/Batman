<script setup lang="ts">
import { ElTable, ElTableColumn, ElButton, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import type { PropType } from 'vue'
import {
  type AlgorithmItem,
  AlgorithmCategoryDefinitions,
  AlgorithmTypeDefinitions,
  AlgorithmStockListDefinitions,
  AlgorithmDataPeriodDefinitions,
  AlgorithmReportPeriodDefinitions
} from '@/api/calc'
import dayjs from 'dayjs'

defineProps({
  tableData: {
    type: Array as PropType<AlgorithmItem[]>,
    required: true
  }
})

const emit = defineEmits(['delete'])

const router = useRouter()

const goToTrendArgument = () => {
  router.push({ name: 'TrendArgument' })
}

const handleDelete = (id: number) => {
  ElMessageBox.confirm('此操作将永久删除该项, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      emit('delete', id)
    })
    .catch(() => {
      // catch cancel
    })
}
</script>

<template>
  <div>
    <div style="margin-bottom: 10px;">
      <el-button type="primary" @click="goToTrendArgument">新增</el-button>
    </div>
    <el-table :data="tableData" style="width: 85%" :border="true">
      <el-table-column prop="id" label="标识" width="60" />
      <el-table-column prop="name" label="名称" width="160" />
      <el-table-column prop="category" label="算法分类" width="100">
        <template #default="{ row }">
          {{ AlgorithmCategoryDefinitions[row.category]?.title }}
        </template>
      </el-table-column>
      <el-table-column prop="type" label="算法类型" width="120">
        <template #default="{ row }">
          {{ AlgorithmTypeDefinitions[row.type]?.title }}
        </template>
      </el-table-column>
      <el-table-column prop="list_type" label="列表类型" width="100">
        <template #default="{ row }">
          {{ AlgorithmStockListDefinitions[row.list_type] }}
        </template>
      </el-table-column>
      <el-table-column prop="data_period" label="数据周期" width="100">
        <template #default="{ row }">
          {{ AlgorithmDataPeriodDefinitions[row.data_period] }}
        </template>
      </el-table-column>
      <el-table-column prop="report_period" label="报告周期" width="100">
        <template #default="{ row }">
          {{ AlgorithmReportPeriodDefinitions[row.report_period] }}
        </template>
      </el-table-column>
      <el-table-column prop="remarks" label="备注" />
      <el-table-column prop="created" label="更新日期" width="180">
        <template #default="{ row }">
          {{ dayjs(row.created).format('YYYY-MM-DD HH:mm:ss') }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button type="text">详情</el-button>
          <el-button type="text" style="color: red;" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped>
</style>