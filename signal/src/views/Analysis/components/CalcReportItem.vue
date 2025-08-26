<script setup lang="ts">
import type { PropType } from 'vue'
import { ElCard, ElDescriptions, ElDescriptionsItem, ElTag } from 'element-plus'
import type { CalcReportSseData } from '@/api/calc'

defineProps({
  reportData: {
    type: Object as PropType<CalcReportSseData>,
    required: true
  }
})
</script>

<template>
  <div class="calc-report-item">
    <el-card>
      <el-descriptions border :column="3">
        <el-descriptions-item label="代码">{{ reportData.code }}</el-descriptions-item>
        <el-descriptions-item label="名称">{{ reportData.name }}</el-descriptions-item>
        <el-descriptions-item label="日期">{{ reportData.date }}</el-descriptions-item>
        <el-descriptions-item label="标记">
          <el-tag>{{ reportData.flag }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="数据" :span="2">
          <pre>{{ reportData.data }}</pre>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<style scoped>
.calc-report-item {
  margin-bottom: 1rem;
}
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
