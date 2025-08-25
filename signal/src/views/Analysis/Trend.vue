<script setup lang="ts">
import { ref, onMounted, watch, onActivated, nextTick } from 'vue'
import { ElSelect, ElOption, ElButton, ElDivider, ElMessage } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import TrendArgumentTable from './components/TrendArgumentTable.vue'
import CalcReport from './components/CalcReport.vue'
import AlgorithmItemDetail from './components/AlgorithmItemDetail.vue'
import { apiListAlgorithmItems, apiDeleteAlgorithmItem, apiSubmitCalculation, AlgorithmItem } from '@/api/calc'
import { useRefreshStore } from '@/store/modules/refresh'

const selectedValue = ref('')
const selectedAlgorithmItem = ref<AlgorithmItem | null>(null)

const showArgumentTable = ref(false)
const algorithmItems = ref<AlgorithmItem[]>([])
const calcReportRef = ref<InstanceType<typeof CalcReport> | null>(null)
const showCalcReport = ref(false)

const getAlgorithmItems = async () => {
  const res = await apiListAlgorithmItems({})
  if (res) {
    algorithmItems.value = res.result
  }
}

onMounted(() => {
  getAlgorithmItems().then(() => {
    showArgumentTable.value = algorithmItems.value.length === 0
  })
})

onActivated(() => {
  const refreshStore = useRefreshStore()
  if (refreshStore.needsRefresh) {
    getAlgorithmItems().then(() => {
      showArgumentTable.value = true
    })
    refreshStore.setNeedsRefresh(false)
  }
})

watch(selectedValue, (newValue) => {
  // Reset the calculation result view whenever the selection changes
  if (showCalcReport.value) {
    calcReportRef.value?.disconnect()
    showCalcReport.value = false
  }

  if (newValue) {
    // Update the selected item details based on the new selection
    if (newValue !== selectedAlgorithmItem.value?.name) {
      selectedAlgorithmItem.value = algorithmItems.value.find((item) => item.name === newValue) || null
    }
  } else {
    // If selection is cleared, ensure item is also cleared
    selectedAlgorithmItem.value = null
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

const handleRowSelect = (item: AlgorithmItem) => {
  selectedValue.value = item.name
  selectedAlgorithmItem.value = item
}

const handleSubmit = async () => {
  if (!selectedValue.value || !selectedAlgorithmItem.value) {
    ElMessage.warning('请选择一个项目')
    return
  }

  const res = await apiSubmitCalculation({ id: selectedAlgorithmItem.value.id! })
  if (res) {
    if (res.result === 0) {
      ElMessage.success(`已成功提交 '${selectedAlgorithmItem.value.name}' 进行计算。`)
      showCalcReport.value = true
      showArgumentTable.value = false
      nextTick(() => {
        calcReportRef.value?.connect()
      })
    } else {
      ElMessage.warning(`任务 '${selectedAlgorithmItem.value.name}' 已在运行中，请勿重复提交。`)
    }
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
      <el-button type="primary" style="margin-left: 10px;" :disabled="!selectedValue" @click="handleSubmit">提交</el-button>
      <el-button @click="toggleTable">{{ showArgumentTable ? '收起列表' : '查看列表' }}</el-button>
    </div>
    <TrendArgumentTable
      v-if="showArgumentTable"
      :table-data="algorithmItems"
      @delete="handleDeleteItem"
      @select="handleRowSelect"
    />

    <el-divider />

    <AlgorithmItemDetail v-if="showCalcReport" :item="selectedAlgorithmItem" />
    <CalcReport v-if="showCalcReport" ref="calcReportRef" :item-id="selectedAlgorithmItem!.id!" />
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