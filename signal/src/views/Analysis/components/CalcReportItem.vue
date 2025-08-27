<script setup lang="ts">
import type { PropType } from 'vue'
import { ElCard, ElDescriptions, ElDescriptionsItem, ElTag } from 'element-plus'
import type { CalcReportSseData } from '@/api/calc'

defineProps({
  data: {
    type: Object as PropType<CalcReportSseData>,
    required: true
  }
})
</script>

<template>
  <div class="calc-report-item">
    <el-card>
      <el-descriptions :border="true" :column="3">
        <el-descriptions-item label="代码">{{ data.stock.code }}</el-descriptions-item>
        <el-descriptions-item label="名称">{{ data.stock.name }}</el-descriptions-item>
        <!-- <el-descriptions-item label="日期">{{ data.date }}</el-descriptions-item> -->
        <el-descriptions-item label="类别">
          <el-tag>{{ data.category }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="类型" :span="2">
          <pre>{{ data.type }}</pre>
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
