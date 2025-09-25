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
  ElTree,
  ElMessage,
  type ElTree as ElTreeType
} from 'element-plus'
import AlgorithmCategory from './components/AlgorithmCategory.vue'
import { TYPE_STOCK } from '@/api/data'
import {
  AlgorithmCategoryDefinitions,
  AlgorithmCategoryOptionType,
  AlgorithmDataPeriodDefinitions,
  AlgorithmReportPeriodDefinitions,
  AlgorithmStockListDefinitions,
  AlgorithmTypeDefinitions
} from '@/api/calc/defines'
import type { AlgorithmItem, ArgumentItem, StockListItem } from '@/api/calc/types'
import {
  apiCreateAlgorithmItem,
  apiListStockList,
  apiCreateStockList,
  apiCreateArguments,
  apiGetAlgorithmItem,
  apiListArguments,
  apiUpdateStockList,
  apiUpdateArguments,
  apiUpdateAlgorithmItem
} from '@/api/calc'
import { apiRecord } from '@/api/holding'
import { apiRecords } from '@/api/customized'
import ItemSearchDialog from '@/views/Common/components/ItemSearchDialog.vue'
import { useRefreshStore } from '@/store/modules/refresh'

interface StockListTableItem extends Pick<StockListItem, 'type' | 'code' | 'name'> {
  src: number
}

const props = defineProps({
  id: {
    type: Number,
    required: false
  }
})

const router = useRouter()
const refreshStore = useRefreshStore()
const effectiveId = computed(() => props.id || history.state.id)

const goBack = () => {
  router.back()
}

const formData = reactive<Omit<AlgorithmItem, 'id' | 'uid' | 'created'>>({
  name: '',
  remarks: '',
  list_type: 4, // holding + watchlist
  data_period: 1, // 6m
  report_period: 1, // 3d
  show_opt: 1
})

const isSubmitDisabled = computed(() => !formData.name || formData.name.trim() === '')

const tableData = ref<StockListTableItem[]>([])

const loadStockList = async () => {
  const listType = formData.list_type
  let stocks: StockListTableItem[] = tableData.value

  const fetchHolding = async () => {
    try {
      const res = await apiRecord({})
      return res.result.map((item) => ({ ...item, src: 0 }))
    } catch (error) {
      ElMessage.error('获取持仓列表失败')
      return []
    }
  }

  const fetchCustomized = async () => {
    try {
      const res = await apiRecords({})
      return res.result.map((item) => ({ ...item, src: 1 }))
    } catch (error) {
      ElMessage.error('获取自选列表失败')
      return []
    }
  }

  if (listType === 0) {
    const holdingStocks = await fetchHolding()
    stocks = Array.from(new Map(holdingStocks.map((item) => [item.code, item])).values())
  } else if (listType === 1) {
    const customizedStocks = await fetchCustomized()
    stocks = Array.from(new Map(customizedStocks.map((item) => [item.code, item])).values())
  } else if (listType === 2) {
    if (effectiveId.value) {
      try {
        const res = await apiListStockList({ cid: effectiveId.value })
        stocks = res.result.map((item) => ({ ...item, src: 2 }))
      } catch (error) {
        ElMessage.error('获取算法自定义列表失败')
        tableData.value = []
      }
    }
  } else if (listType === 3) {
    stocks = []
  } else if (listType === 4) {
    const holdingStocks = await fetchHolding()
    const customizedStocks = await fetchCustomized()
    const combined = [...holdingStocks, ...customizedStocks]
    stocks = Array.from(new Map(combined.map((item) => [item.code, item])).values())
  }

  tableData.value = stocks
}

const populateDisplayedCategories = (args: ArgumentItem[]) => {
  const groupedByCategory: Record<string, ArgumentItem[]> = {}
  args.forEach((arg) => {
    if (!groupedByCategory[arg.category]) {
      groupedByCategory[arg.category] = []
    }
    groupedByCategory[arg.category].push(arg)
  })

  const result: typeof displayedCategories.value = []

  for (const catKey in groupedByCategory) {
    const categoryArgs = groupedByCategory[catKey]
    const categoryDefinition = AlgorithmCategoryDefinitions[catKey]
    if (!categoryDefinition) continue

    const types = categoryArgs.map((arg) => {
      const params = JSON.parse(arg.arguments)
      const typeDefinition = AlgorithmTypeDefinitions[catKey]?.types?.[arg.type]
      let options: Array<{ option: AlgorithmCategoryOptionType; value?: any }> = []
      if (typeDefinition && typeDefinition.options) {
        options = typeDefinition.options.map((optDef) => ({
          option: optDef,
          value: params[optDef.name]
        }))
      }
      return {
        id: nextTypeId++,
        key: arg.type,
        options: options
      }
    })

    result.push({
      categoryKey: catKey,
      types: types
    })
  }
  displayedCategories.value = result
}

watch(
  effectiveId,
  async (id) => {
    if (id) {
      try {
        const itemRes = await apiGetAlgorithmItem({ id })
        if (itemRes.result) {
          Object.assign(formData, itemRes.result)
        } else {
          ElMessage.error('Algorithm item not found.')
          router.back()
          return
        }
        await loadStockList()
        const argsRes = await apiListArguments({ cid: id })
        populateDisplayedCategories(argsRes.result)
      } catch (error) {
        ElMessage.error('Failed to load algorithm data.')
      }
    } else {
      Object.assign(formData, {
        name: '',
        remarks: '',
        list_type: 4,
        data_period: 1,
        report_period: 1,
        show_opt: 1
      })
      loadStockList()
    }
  },
  { immediate: true }
)

const stockListUi = ref<string[]>([])
const dataPeriodUi = ref<string[]>([])
const reportRangeUi = ref<string[]>([])

const listTypeFromNumber = (t: number | undefined) => {
  if (t === undefined) return [AlgorithmStockListDefinitions[3]]
  if (t === 4) return [AlgorithmStockListDefinitions[0], AlgorithmStockListDefinitions[1]]
  return [AlgorithmStockListDefinitions[t]]
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

const handleStockListChange = (val: string[]) => {
  if (!val || val.length === 0) {
    stockListUi.value = [AlgorithmStockListDefinitions[formData.list_type]]
    return
  }
  const newSelection = [...val]
  const lastSelection = newSelection.at(-1)
  const holding = AlgorithmStockListDefinitions[0]
  const watchlist = AlgorithmStockListDefinitions[1]
  const custom = AlgorithmStockListDefinitions[2]
  const all = AlgorithmStockListDefinitions[3]

  if (lastSelection === custom) {
    stockListUi.value = [custom]
    formData.list_type = 2
    return // Do not call loadStockList, preserving tableData
  } else if (lastSelection === all) {
    stockListUi.value = [all]
  } else {
    stockListUi.value = newSelection.filter((item) => item === holding || item === watchlist)
  }

  const selection = stockListUi.value
  const hasHolding = selection.includes(holding)
  const hasWatchlist = selection.includes(watchlist)

  if (hasHolding && hasWatchlist) {
    formData.list_type = 4
  } else if (hasHolding) {
    formData.list_type = 0
  } else if (hasWatchlist) {
    formData.list_type = 1
  } else if (selection.includes(custom)) {
    formData.list_type = 2
  } else if (selection.includes(all)) {
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
const showStockTable = computed(() => !stockListUi.value.includes(AlgorithmStockListDefinitions[3]))
const showStockTableAddButton = computed(() =>
  stockListUi.value.includes(AlgorithmStockListDefinitions[2])
)

const canDeleteStock = computed(() => {
  return stockListUi.value.includes(AlgorithmStockListDefinitions[2])
})

const quickViewDialogVisible = ref(false)
const handleAddStockClick = () => {
  quickViewDialogVisible.value = true
}

const onQuickViewConfirm = (item: { code: string; name: string; type: number }) => {
  if (tableData.value.some((i) => i.code === item.code && i.type === item.type)) {
    ElMessage.warning('代码已存在')
    return
  }
  tableData.value.push({ ...item, src: 2 })
  quickViewDialogVisible.value = false
}

const treeData = computed(() => {
  return Object.keys(AlgorithmCategoryDefinitions).map((catKey) => {
    const category = AlgorithmCategoryDefinitions[catKey]
    const typesForCategory = AlgorithmTypeDefinitions[catKey]?.types || {}
    const children = Object.keys(typesForCategory).map((typeKey) => {
      const type = typesForCategory[typeKey]
      return {
        value: `${catKey}-${typeKey}`,
        label: `${type.title} - ${type.description}`
      }
    })
    return {
      value: catKey,
      label: `${category.title}(${catKey}) - ${category.description}`,
      children: children,
      disabled: true
    }
  })
})

const displayedCategories = ref<
  Array<{
    categoryKey: string
    types: Array<{
      id: number
      key: string
      options: Array<{
        option: AlgorithmCategoryOptionType
        value?: any
      }>
    }>
  }>
>([])

let nextTypeId = 0

const addAlgorithm = (value: string) => {
  if (!value) return
  const parts = value.split('-')
  if (parts.length !== 2) {
    return
  }
  const [catKey, typeKey] = parts
  let existingCategory = displayedCategories.value.find((c) => c.categoryKey === catKey)
  if (!existingCategory) {
    existingCategory = { categoryKey: catKey, types: [] }
    displayedCategories.value.push(existingCategory)
  }
  const typeDefinition = AlgorithmTypeDefinitions[catKey]?.types?.[typeKey]
  const typeOptions: Array<{ option: AlgorithmCategoryOptionType; value?: any }> = []
  if (typeDefinition && typeDefinition.options) {
    typeDefinition.options.forEach((option) => {
      typeOptions.push({ option: option, value: option.default })
    })
  }
  existingCategory.types.push({ id: nextTypeId++, key: typeKey, options: typeOptions })
}

const handleDeleteType = (event: { categoryKey: string; typeKey: string }) => {
  const { categoryKey, typeKey } = event
  const category = displayedCategories.value.find((c) => c.categoryKey === categoryKey)
  if (category) {
    const typeIndex = category.types.findIndex((t) => t.key === typeKey)
    if (typeIndex > -1) {
      category.types.splice(typeIndex, 1)
    }
    if (category.types.length === 0) {
      const catIndex = displayedCategories.value.findIndex((c) => c.categoryKey === categoryKey)
      if (catIndex > -1) {
        displayedCategories.value.splice(catIndex, 1)
      }
    }
  }
}

const handleDeleteStock = (index: number) => {
  tableData.value.splice(index, 1)
}

const submitForm = async () => {
  try {
    if (effectiveId.value) {
      await apiUpdateAlgorithmItem({
        id: effectiveId.value,
        name: formData.name,
        remarks: formData.remarks,
        list_type: formData.list_type,
        data_period: formData.data_period,
        report_period: formData.report_period,
        show_opt: formData.show_opt
      })
      if (showStockTableAddButton.value) {
        const items = tableData.value.map((item) => ({
          type: item.type,
          code: item.code,
          name: item.name
        }))
        await apiUpdateStockList({ cid: effectiveId.value, items: items })
      }
      const args: ArgumentItem[] = []
      displayedCategories.value.forEach((category) => {
        category.types.forEach((type) => {
          const params: Record<string, any> = {}
          type.options.forEach((opt) => {
            params[opt.option.name] = opt.value
          })
          args.push({
            cid: effectiveId.value as number,
            category: category.categoryKey,
            type: type.key,
            arguments: JSON.stringify(params)
          })
        })
      })
      await apiUpdateArguments({ cid: effectiveId.value, items: args })
      ElMessage.success('更新成功')
    } else {
      const res = await apiCreateAlgorithmItem(formData)
      const cid = res.result
      if (showStockTableAddButton.value) {
        const items = tableData.value.map((item) => ({
          type: item.type,
          code: item.code,
          name: item.name
        }))
        await apiCreateStockList({ cid: cid, items: items })
      }
      const args: ArgumentItem[] = []
      displayedCategories.value.forEach((category) => {
        category.types.forEach((type) => {
          const params: Record<string, any> = {}
          type.options.forEach((opt) => {
            params[opt.option.name] = opt.value
          })
          args.push({
            cid: cid,
            category: category.categoryKey,
            type: type.key,
            arguments: JSON.stringify(params)
          })
        })
      })
      await apiCreateArguments({ cid: cid, items: args })
      ElMessage.success('提交成功')
    }
    refreshStore.setNeedsRefresh(true)
    router.back()
  } catch (error) {
    ElMessage.error('提交失败')
  }
}

const isTreeExpanded = ref(false)
const algorithmTreeRef = ref<InstanceType<typeof ElTreeType> | null>(null)

const toggleTreeExpansion = () => {
  isTreeExpanded.value = !isTreeExpanded.value
  const tree = algorithmTreeRef.value
  if (!tree) return
  for (const key in tree.store.nodesMap) {
    if (Object.prototype.hasOwnProperty.call(tree.store.nodesMap, key)) {
      tree.store.nodesMap[key].expanded = isTreeExpanded.value
    }
  }
}
</script>

<template>
  <ContentDetailWrap title="设置计算参数">
    <template #header>
      <div class="header-container">
        <ElButton type="primary" @click="goBack">返回</ElButton>
        <ElButton type="danger" @click="submitForm" :disabled="isSubmitDisabled">提交</ElButton>
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
      <el-col :span="8" style="padding-right: 20px; border-right: 1px solid var(--el-border-color)">
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
          <el-table
            v-if="showStockTable"
            :data="tableData"
            style="width: 100%; margin-top: 10px"
            :border="true"
          >
            <el-table-column type="index" label="序号" width="60" />
            <el-table-column prop="type" label="类型" width="60">
              <template #default="scope">
                <span>{{ scope.row.type === TYPE_STOCK ? '股票' : '指数' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="code" label="代码" />
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
            <el-checkbox label="最近一天" value="最近一天" />
            <el-checkbox label="最近三天" value="最近三天" />
            <el-checkbox label="最近一周" value="最近一周" />
            <el-checkbox label="最近一月" value="最近一月" />
            <el-checkbox label="全部" value="全部" />
          </el-checkbox-group>
        </div>

        <div style="margin-top: 20px">
          <div class="section-title">显示参数</div>
          <el-checkbox
            v-model="formData.show_opt"
            label="显示计算结果图表"
            :true-value="1"
            :false-value="0"
          />
        </div>
      </el-col>

      <!-- Right Column -->
      <el-col :span="16" style="padding-left: 20px">
        <el-row>
          <el-col>
            <div
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
              "
            >
              <div class="section-title" style="margin-bottom: 0">算法选择</div>
              <el-button size="small" @click="toggleTreeExpansion">{{
                isTreeExpanded ? '收起' : '展开'
              }}</el-button>
            </div>
            <div
              style="
                padding: 5px;
                margin-bottom: 20px;
                border: 1px solid var(--el-border-color);
                border-radius: 4px;
              "
            >
              <el-tree
                ref="algorithmTreeRef"
                :data="treeData"
                :expand-on-click-node="true"
              >
                <template #default="{ node, data }">
                  <span class="custom-tree-node" style="justify-content: flex-start;">
                    <el-button
                      v-if="!data.disabled"
                      @click.stop="addAlgorithm(data.value)"
                      size="small"
                      style="margin-right: 6px;"
                    >
                      添加
                    </el-button>
                    <span>{{ node.label }}</span>
                  </span>
                </template>
              </el-tree>
            </div>
            <div v-for="(category, index) in displayedCategories" :key="category.categoryKey">
              <AlgorithmCategory
                :category-key="category.categoryKey"
                :types="category.types"
                :index="index + 1"
                @delete-type="handleDeleteType"
              />
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

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
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: 700;
}

.custom-tree-node {
  display: flex;
  padding-right: 8px;
  font-size: 14px;
  flex: 1;
  align-items: center;
  /* justify-content: space-between; */
  justify-content: flex-start;
}
</style>
