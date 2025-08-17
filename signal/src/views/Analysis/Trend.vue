<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElSelect, ElOption, ElButton, ElDivider, ElMessage } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import TrendArgumentTable from './components/TrendArgumentTable.vue'
import { apiListAlgorithmItems, apiDeleteAlgorithmItem, AlgorithmItem } from '@/api/calc'

const selectedValue = ref('')

const showArgumentTable = ref(false)
const algorithmItems = ref<AlgorithmItem[]>([])

const getAlgorithmItems = async () => {
  const res = await apiListAlgorithmItems({})
  if (res) {
    algorithmItems.value = res.result
    showArgumentTable.value = algorithmItems.value.length === 0
  }
}

onMounted(() => {
  getAlgorithmItems()
})

watch(selectedValue, (newValue) => {
  if (!newValue) {
    showArgumentTable.value = true
  }
})

const toggleTable = () => {
  showArgumentTable.value = !showArgumentTable.value
}

const handleDeleteItem = async (id: number) => {
  const res = await apiDeleteAlgorithmItem({ id })
  if (res) {
    ElMessage.success('删除成功')
    getAlgorithmItems()
  }
}
</script>

<template>
  <ContentWrap>
    <div class="section-title">计算列表</div>
    <div class="action-container">
      <el-select v-model="selectedValue" placeholder="Select" class="select-width" clearable>
        <el-option
          v-for="item in algorithmItems"
          :key="item.id"
          :label="item.name"
          :value="item.name"
        />
      </el-select>
      <el-button type="primary" style="margin-left: 10px;" :disabled="!selectedValue">提交</el-button>
      <el-button @click="toggleTable">{{ showArgumentTable ? '收起列表' : '查看列表' }}</el-button>
    </div>
    <TrendArgumentTable
      v-if="showArgumentTable"
      :table-data="algorithmItems"
      @delete="handleDeleteItem"
    />

    <el-divider />

    <div class="section-title">计算结果</div>
    <!-- Content for calculation results goes here -->
  </ContentWrap>
</template>

<style scoped>
.section-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 10px;
}
.action-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.select-width {
  width: 33.33%;
}
</style>