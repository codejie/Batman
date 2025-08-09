<script setup lang="ts">
import { ref } from 'vue'
import { ElTable, ElTableColumn, ElButton } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

const tableData = ref([
  {
    id: '1',
    name: '参数1',
    remarks: '这是一个备注',
    updateDate: '2025-08-09'
  },
  {
    id: '2',
    name: '参数2',
    remarks: '这是另一个备注',
    updateDate: '2025-08-08'
  }
])

const goToTrendArgument = () => {
  router.push({ name: 'TrendArgument' })
}
</script>

<template>
  <div>
    <div style="margin-bottom: 10px;">
      <el-button type="primary" @click="goToTrendArgument">新增</el-button>
    </div>
    <el-table :data="tableData" style="width: 85%" :border="true">
      <el-table-column prop="id" label="标识" width="60" />
      <el-table-column prop="name" label="名称" width="200" />
      <el-table-column prop="remarks" label="备注" />
      <el-table-column prop="updateDate" label="更新日期" width="160" />
      <el-table-column label="操作" width="160">
        <template #default>
          <el-button type="text">详情</el-button>
          <el-button type="text" style="color: red;">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped>
</style>