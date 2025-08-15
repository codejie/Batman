<script setup lang="ts">
import { reactive, ref, computed, watch } from 'vue'
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { useRouter } from 'vue-router'
import {
  ElButton,
  ElForm,
  ElFormItem,
  ElInput,
  ElRow,
  ElCol,
  ElCheckboxGroup,
  ElCheckbox,
  ElTable,
  ElTableColumn,
  ElDivider,
  ElTreeSelect,
  ElDialog,
  ElMessage
} from 'element-plus'
import AlgorithmCategory from './components/AlgorithmCategory.vue'
import { TYPE_STOCK } from '@/api/data'
import {
  AlgorithmCategoryDefinitions,
  AlgorithmDataPeriodDefinitions,
  AlgorithmReportPeriodDefinitions,
  AlgorithmStockListDefinitions,
  AlgorithmTypeDefinitions
} from '@/api/calc/defines'
import type { PropType } from 'vue'
import type { AlgorithmItem, StockListItem } from '@/api/calc/types'
import { apiCreateAlgorithmItem, apiListStockList, apiCreateStockList } from '@/api/calc'
import { apiRecord } from '@/api/holding'
import { apiRecords } from '@/api/customized'
import ItemSearchDialog from '@/views/Common/components/ItemSearchDialog.vue'

interface StockListTableItem extends Pick<StockListItem, 'type' | 'code' | 'name'> {
  src: number
}

const props = defineProps({
  item: {
    type: Object as PropType<AlgorithmItem>,
    required: false
  }
})

const router = useRouter()

const goBack = () => {
  router.back()
}

const formData = reactive<Omit<AlgorithmItem, 'id' | 'uid' | 'created'>>({
  name: '',
  remarks: '',
  category: 0,
  type: 0,
  list_type: 4, // all
  data_period: 1, // 6m
  report_period: 1 // 3d
})

const loadStockList = async (isInitialLoad = false) => {
  const listType = formData.list_type

  // '自定义列表'
  if (listType === 2) {
    if (isInitialLoad && props.item?.id) {
      try {
        const res = await apiListStockList({ cid: props.item.id })
        const stocks = res.result.map((item) => ({
          ...item,
          src: 2
        }))
        tableData.value = Array.from(new Map(stocks.map((item) => [item.code, item])).values())
      } catch (error) {
        ElMessage.error('获取算法自定义列表失败')
        tableData.value = []
      }
    }
    // On user switch to '自定义列表' (isInitialLoad = false), do nothing to preserve table data.
    // If creating a new item with type 2 (isInitialLoad = true, no props.item.id), do nothing, table is empty.
    return
  }

  tableData.value = []
  let stocks: StockListTableItem[] = []

  const fetchHolding = async () => {
    try {
      const res = await apiRecord({})
      return res.result.map((item) => ({ ...item, src: 0 }))
    } catch (error) {
      ElMessage.error('获取持仓列表失败')
      console.error(error)
      return []
    }
  }

  const fetchCustomized = async () => {
    try {
      const res = await apiRecords({})
      return res.result.map((item) => ({ ...item, src: 1 }))
    } catch (error) {
      ElMessage.error('获取自选列表失败')
      console.error(error)
      return []
    }
  }

  if (listType === 0) {
    // '持仓列表'
    const holdingStocks = await fetchHolding()
    stocks = Array.from(new Map(holdingStocks.map((item) => [item.code, item])).values())
  } else if (listType === 1) {
    // '自选列表'
    const customizedStocks = await fetchCustomized()
    stocks = Array.from(new Map(customizedStocks.map((item) => [item.code, item])).values())
  } else if (listType === 4) {
    // '持仓列表' + '自选列表'
    const holdingStocks = await fetchHolding()
    const customizedStocks = await fetchCustomized()
    const combined = [...holdingStocks, ...customizedStocks]
    stocks = Array.from(new Map(combined.map((item) => [item.code, item])).values())
  }

  tableData.value = stocks
}

watch(
  () => props.item,
  (newItem) => {
    if (newItem) {
      Object.assign(formData, newItem)
    }
    loadStockList(true)
  },
  { immediate: true }
)

// UI State
const stockListUi = ref<string[]>([])
const dataPeriodUi = ref<string[]>([])
const reportRangeUi = ref<string[]>([])

// Mapping and Sync Logic
const listTypeFromNumber = (t: number | undefined) => {
  if (t === undefined) return []
  if (t === 4) return ['持仓列表', '自选列表'] // Special case
  const def = AlgorithmStockListDefinitions[t]
  return def ? [def] : []
}

watch(
  formData,
  (currentForm) => {
    stockListUi.value = listTypeFromNumber(currentForm.list_type)
    dataPeriodUi.value = [AlgorithmDataPeriodDefinitions[currentForm.data_period]]
    reportRangeUi.value = [AlgorithmReportPeriodDefinitions[currentForm.report_period]]
  },
  { immediate: true, deep: true }
)

// Event Handlers
const handleStockListChange = (val: string[]) => {
  const customList = '自定义列表'
  const allListsValue = '全部列表'

  let newSelection = val ? [...val] : []
  const lastSelection = newSelection.at(-1)

  if (lastSelection === customList) {
    newSelection = [customList]
  } else if (lastSelection === allListsValue) {
    newSelection = [allListsValue]
  } else if (lastSelection) {
    // any other selection
    newSelection = newSelection.filter((i) => i !== customList && i !== allListsValue)
  }

  stockListUi.value = newSelection

  // Convert UI selection to formData
  if (newSelection.includes('持仓列表') && newSelection.includes('自选列表')) {
    formData.list_type = 4 // Special case for holding + watchlist
  } else if (newSelection.includes(customList)) {
    formData.list_type = 2
  } else if (newSelection.includes('持仓列表')) {
    formData.list_type = 0
  } else if (newSelection.includes('自选列表')) {
    formData.list_type = 1
  } else if (newSelection.includes(allListsValue)) {
    formData.list_type = 3
  }

  loadStockList()
}

const handleDataPeriodChange = (val: string[]) => {
  if (!val || val.length === 0) {
    dataPeriodUi.value = [AlgorithmDataPeriodDefinitions[formData.data_period]]
    return
  }
  const index = AlgorithmDataPeriodDefinitions.indexOf(val[val.length - 1])
  if (index !== -1) {
    formData.data_period = index
  }
}

const handleReportRangeChange = (val: string[]) => {
  if (!val || val.length === 0) {
    reportRangeUi.value = [AlgorithmReportPeriodDefinitions[formData.report_period]]
    return
  }
  const index = AlgorithmReportPeriodDefinitions.indexOf(val[val.length - 1])
  if (index !== -1) {
    formData.report_period = index
  }
}

const tableData = ref<StockListTableItem[]>([])
const showStockTable = computed(() =>
  !stockListUi.value.includes('全部列表')
)
const showStockTableAddButton = computed(() =>
  stockListUi.value.includes('自定义列表')
)

const canDeleteStock = computed(() => {
  return stockListUi.value.includes('自定义列表')
})

const quickViewDialogVisible = ref(false)

const handleAddStockClick = () => {
  quickViewDialogVisible.value = true
}

const onQuickViewConfirm = (item: { code: string; name: string; type: number }) => {
  if (tableData.value.some((i) => i.code === item.code)) {
    ElMessage.warning('代码已存在')
    return
  }
  tableData.value.push({
    ...item,
    src: 2 // 自定义
  })
  quickViewDialogVisible.value = false
}

// const submitAddStockForm = async () => {
//   const form = addStockFormRef.value
//   if (!form) return
//   await form.validate()

//   try {
//     const res = await apiGetCode({ code: addStockFormData.code })
//     if (res.result) {
//       const newItem: StockListItem = {
//         code: res.result.code,
//         name: res.result.name,
//         type: res.result.type
//       }
//       if (tableData.value.some((item) => item.code === newItem.code)) {
//         ElMessage.warning('代码已存在')
//         return
//       }
//       tableData.value.push(newItem)
//       addStockDialogVisible.value = false
//     } else {
//       ElMessage.error('无效的代码')
//     }
//   } catch (error) {
//     console.error(error)
//     ElMessage.error('获取代码信息失败')
//   }
// }

const mockCategory = ref({
  name: 'MA',
  title: '均线',
  description: 'Moving Average (MA) - 移动平均线',
  options: []
})

const mockTypes = ref([
  {
    category: 0,
    name: 'MA_MA',
    title: '基础移动均线',
    description: 'Moving Average (MA) - 移动平均线'
  },
  {
    category: 0,
    name: 'EMA',
    title: '指数移动平均线',
    description: 'Exponential Moving Average (EMA) - 指数移动平均线'
  }
])

const treeData = computed(() => {
  return Object.keys(AlgorithmCategoryDefinitions).map((catKey) => {
    const category = AlgorithmCategoryDefinitions[catKey]
    const children = Object.keys(AlgorithmTypeDefinitions)
      .filter((typeKey) => AlgorithmTypeDefinitions[typeKey].category === parseInt(catKey))
      .map((typeKey) => {
        const type = AlgorithmTypeDefinitions[typeKey]
        return {
          value: `type-${typeKey}`,
          label: `${type.title} - ${type.description}`
        }
      })

    return {
      value: `cat-${catKey}`,
      label: `${category.title} - ${category.description}`,
      children: children,
      disabled: true
    }
  })
})

const selectedAlgorithm = ref<string[]>([])
const dialogVisible = ref(false)
const selectedInfo = ref<Array<{ categoryId: string | null; typeId: string | null }>>([])

const handleAddClick = () => {
  selectedInfo.value = []
  const selectedValues = selectedAlgorithm.value

  if (selectedValues && selectedValues.length > 0) {
    selectedValues.forEach((selectedValue) => {
      const info: { categoryId: string | null; typeId: string | null } = { categoryId: null, typeId: null }
      if (selectedValue.startsWith('cat-')) {
        info.categoryId = selectedValue.replace('cat-', '')
      } else if (selectedValue.startsWith('type-')) {
        const typeId = selectedValue.replace('type-', '')
        for (const category of treeData.value) {
          if (category.children && category.children.some((c) => c.value === selectedValue)) {
            info.categoryId = category.value.replace('cat-', '')
            info.typeId = typeId
            break
          }
        }
      }
      if (info.categoryId || info.typeId) {
        selectedInfo.value.push(info)
      }
    })
  }
  dialogVisible.value = true
}

const handleDeleteStock = (index: number) => {
  tableData.value.splice(index, 1)
}

const submitForm = async () => {
  try {
    const res = await apiCreateAlgorithmItem(formData)
    if (showStockTableAddButton.value) {
      await apiCreateStockList({ cid: res.result, items: tableData.value })
    }
    ElMessage.success('提交成功')
    router.back()
  } catch (error) {
    ElMessage.error('提交失败')
    console.error(error)
  }
}
</script>

<template>
  <ContentDetailWrap title="设置计算参数">
    <template #header>
      <div class="header-container">
        <ElButton type="primary" @click="goBack">返回</ElButton>
        <ElButton type="danger" @click="submitForm">提交</ElButton>
      </div>
    </template>

    <!-- Top Section -->
    <el-form :model="formData" label-width="80px">
      <el-row :gutter="24">
        <el-col :span="6">
          <el-form-item class="section-title" label="名称">
            <el-input v-model="formData.name" />
          </el-form-item>
        </el-col>
        <el-col :span="18">
          <el-form-item class="section-title" label="备注">
            <el-input v-model="formData.remarks" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-divider content-position="left">参数设置</el-divider>

    <!-- Bottom Section -->
    <el-row :gutter="24">
      <!-- Left Column -->
      <el-col :span="8" style="border-right: 1px solid var(--el-border-color); padding-right: 20px">
        <div>
          <div class="section-title">股票列表</div>
          <el-checkbox-group v-model="stockListUi" @change="handleStockListChange">
            <el-checkbox label="持仓列表" value="持仓列表" />
            <el-checkbox label="自选列表" value="自选列表" />
            <el-checkbox label="自定义列表" value="自定义列表" />
            <el-checkbox label="全部列表" value="全部列表" />
          </el-checkbox-group>
          <div v-if="showStockTable && showStockTableAddButton" style="margin-top: 10px">
            <el-button size="small" @click="handleAddStockClick">添加</el-button>
          </div>
          <el-table v-if="showStockTable" :data="tableData" style="width: 100%; margin-top: 10px" :border="true">
            <el-table-column type="index" label="序号" width="60" />
            <el-table-column prop="type" label="类型" width="60">
              <template #default="scope">
                <span>{{ scope.row.type === TYPE_STOCK ? '股票' : '指数' }}</span>
              </template>
            </el-table-column>            
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="code" label="代码" />
            <!-- <el-table-column prop="holding" label="持有" /> -->
            <el-table-column v-if="canDeleteStock" label="操作">
              <template #default="scope">
                <el-button type="danger" size="small" @click="handleDeleteStock(scope.$index)"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div style="margin-top: 20px">
          <div class="section-title">数据期间</div>
          <el-checkbox-group v-model="dataPeriodUi" @change="handleDataPeriodChange">
            <el-checkbox label="三个月" value="三个月" />
            <el-checkbox label="六个月" value="六个月" />
            <el-checkbox label="一年" value="一年" />
            <el-checkbox label="两年" value="两年" />
          </el-checkbox-group>
        </div>

        <div style="margin-top: 20px">
          <div class="section-title">报告期间</div>
          <el-checkbox-group v-model="reportRangeUi" @change="handleReportRangeChange">
            <el-checkbox label="当天" value="当天" />
            <el-checkbox label="最近三天" value="最近三天" />
            <el-checkbox label="最近一周" value="最近一周" />
            <el-checkbox label="最近一月" value="最近一月" />
            <el-checkbox label="全部" value="全部" />
          </el-checkbox-group>
        </div>
      </el-col>

      <!-- Right Column -->
      <el-col :span="16" style="padding-left: 20px">
        <el-row>
          <el-col>
            <div class="section-title">算法参数</div>
            <div style="display: flex; align-items: center; margin-bottom: 20px">
              <el-tree-select
                v-model="selectedAlgorithm"
                :data="treeData"
                placeholder="请选择算法"
                style="flex-grow: 1; margin-right: 10px"
                clearable
                check-strictly
                default-expand-all
                multiple
              />
              <el-button type="primary" @click="handleAddClick">添加</el-button>
            </div>
            <AlgorithmCategory :category-key="'0'" :types="mockTypes" :category-id="0" :index="1" />
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="选中项">
      <div v-if="selectedInfo.length > 0">
        <div v-for="(info, index) in selectedInfo" :key="index">
          <p>--- 第 {{ index + 1 }} 项 ---</p>
          <p v-if="info.categoryId">一级ID: {{ info.categoryId }}</p>
          <p v-if="info.typeId">二级ID: {{ info.typeId }}</p>
        </div>
      </div>
      <p v-else>未选择任何项</p>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <ItemSearchDialog v-model:visible="quickViewDialogVisible" @confirm="onQuickViewConfirm" />
  </ContentDetailWrap>
</template>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.section-title {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 10px;
}
</style>
