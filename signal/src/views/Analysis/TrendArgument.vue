<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
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
  ElDialog
} from 'element-plus'
import AlgorithmCategory from './components/AlgorithmCategory.vue'
import { AlgorithmCategoryDefinitions, AlgorithmTypeDefinitions } from '@/api/calc'

const router = useRouter()

const goBack = () => {
  router.back()
}

const formData = reactive<{
  title: string
  remarks: string
  stockList: string[]
  dataPeriod: string[]
  reportRange: string[]
}>({
  title: '',
  remarks: '',
  stockList: ['all'],
  dataPeriod: ['6m'],
  reportRange: ['3d']
})

const tableData = ref([])
const showStockTable = ref(false) // Default to false since stockList defaults to ['all']
const showStockTableAddButton = ref(false)

const handleStockListChange = (newList: string[]) => {
    if (newList.at(-1) === 'all') {
      formData.stockList = ['all']
      showStockTable.value = false
      showStockTableAddButton.value = false
    } else if (newList.at(-1) === 'custom') {
      formData.stockList = ['custom']
      showStockTable.value = true
      showStockTableAddButton.value = true
    } else if (newList.includes('holding') || newList.includes('watchlist')) {
      formData.stockList = newList.filter(item => (item !== 'all' && item !== 'custom'))
      showStockTable.value = true
      showStockTableAddButton.value = false
    }
}

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
  return Object.keys(AlgorithmCategoryDefinitions).map(catKey => {
    const category = AlgorithmCategoryDefinitions[catKey];
    const children = Object.keys(AlgorithmTypeDefinitions)
      .filter(typeKey => AlgorithmTypeDefinitions[typeKey].category === parseInt(catKey))
      .map(typeKey => {
        const type = AlgorithmTypeDefinitions[typeKey];
        return {
          value: `type-${typeKey}`,
          label: `${type.title} - ${type.description}`
        };
      });

    return {
      value: `cat-${catKey}`,
      label: `${category.title} - ${category.description}`,
      children: children,
      disabled: true
    };
  });
});

const selectedAlgorithm = ref<string | null>(null);
const dialogVisible = ref(false)
const selectedInfo = ref<{ categoryId: string | null, typeId: string | null }>({ categoryId: null, typeId: null })

const handleAddClick = () => {
  selectedInfo.value = { categoryId: null, typeId: null };
  const selectedValue = selectedAlgorithm.value;

  if (selectedValue) {
    if (selectedValue.startsWith('cat-')) {
        selectedInfo.value.categoryId = selectedValue.replace('cat-', '');
    } else if (selectedValue.startsWith('type-')) {
        const typeId = selectedValue.replace('type-', '');
        for (const category of treeData.value) {
            if (category.children && category.children.some(c => c.value === selectedValue)) {
                selectedInfo.value.categoryId = category.value.replace('cat-', '');
                selectedInfo.value.typeId = typeId;
                break;
            }
        }
    }
  }
  dialogVisible.value = true;
};

</script>

<template>
  <ContentDetailWrap title="设置计算参数">
    <template #header>
      <div class="header-container">
        <ElButton type="primary" @click="goBack">返回</ElButton>
        <ElButton type="danger">提交</ElButton>
      </div>
    </template>

    <!-- Top Section -->
    <el-form :model="formData" label-width="80px">
      <el-row :gutter="24">
        <el-col :span="6">
          <el-form-item class="section-title"  label="名称">
            <el-input v-model="formData.title" />
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
      <el-col :span="8" style="border-right: 1px solid var(--el-border-color); padding-right: 20px;">
        <div>
          <div class="section-title">股票列表</div>
          <el-checkbox-group v-model="formData.stockList" @change="handleStockListChange">
            <el-checkbox label="持仓列表" value="holding" />
            <el-checkbox label="自选列表" value="watchlist" />
            <el-checkbox label="自定义列表" value="custom" />
            <el-checkbox label="全部列表" value="all" />
          </el-checkbox-group>
          <div v-if="showStockTable && showStockTableAddButton" style="margin-top: 10px;">
            <el-button size="small">添加</el-button>
          </div>
          <el-table v-if="showStockTable" :data="tableData" style="width: 100%; margin-top: 10px;" :border="true">
            <el-table-column type="index" label="序号" width="60" />
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="code" label="代码" />
            <el-table-column prop="holding" label="持有" />
            <el-table-column prop="holding" label="操作" />
          </el-table>
        </div>

        <div style="margin-top: 20px;">
          <div class="section-title">数据期间</div>
          <el-checkbox-group v-model="formData.dataPeriod">            
            <el-checkbox label="三个月" value="3m" />
            <el-checkbox label="六个月" value="6m" />
            <el-checkbox label="一年" value="1y" />
            <el-checkbox label="两年" value="2y" />
          </el-checkbox-group>
        </div>

        <div style="margin-top: 20px;">
          <div class="section-title">报告期间</div>
          <el-checkbox-group v-model="formData.reportRange">            
            <el-checkbox label="当天" value="today" />
            <el-checkbox label="最近三天" value="3d" />
            <el-checkbox label="最近一周" value="1w" />
            <el-checkbox label="最近一个月" value="1m" />
            <el-checkbox label="全部" value="all" />
          </el-checkbox-group>
        </div>

      </el-col>

      <!-- Right Column -->
      <el-col :span="16" style="padding-left: 20px;">
        <el-row>
          <el-col>
            <div class="section-title">算法参数</div>
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
              <el-tree-select
                v-model="selectedAlgorithm"
                :data="treeData"
                placeholder="请选择算法"
                style="flex-grow: 1; margin-right: 10px;"
                clearable
                check-strictly
                default-expand-all
              />
              <el-button type="primary" @click="handleAddClick">添加</el-button>
            </div>
            <AlgorithmCategory
              :category="mockCategory"
              :types="mockTypes"
              :category-id="0"
            />
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="选中项">
      <p v-if="selectedInfo.categoryId">一级ID: {{ selectedInfo.categoryId }}</p>
      <p v-if="selectedInfo.typeId">二级ID: {{ selectedInfo.typeId }}</p>
      <p v-if="!selectedInfo.categoryId && !selectedInfo.typeId">未选择任何项</p>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

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