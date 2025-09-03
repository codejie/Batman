<script setup lang="ts">
import { AlgorithmCategoryOptionType, AlgorithmTypeDefinitions } from '@/api/calc/defines'
import {
  ElButton,
  ElRow,
  ElCol,
  ElInput,
  ElInputNumber,
  ElSelect,
  ElOption,
  ElDescriptions,
  ElDescriptionsItem,
  ElTooltip
} from 'element-plus'
import { computed, type PropType } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object as PropType<{
        key: string,
        options: Array<{
          option: AlgorithmCategoryOptionType,
          value?: any
        }>
    }>,
    required: true
  },
  index: {
    type: Number,
    required: true
  },
  categoryKey: {
    type: String,
    required: true
  }
})

const typeDefinition = computed(() => {
  return AlgorithmTypeDefinitions[props.categoryKey]?.types?.[props.modelValue.key]
})

const filledOptions = computed(() => {
  const options = props.modelValue.options
  if (!options || options.length === 0) {
    return []
  }
  const filled = [...options]
  const remainder = options.length % 6
  if (remainder > 0) {
    const toAdd = 6 - remainder
    for (let i = 0; i < toAdd; i++) {
      filled.push({ option: { name: '', title: '' } as AlgorithmCategoryOptionType })
    }
  }
  return filled
})

const emit = defineEmits(['delete'])

const handleDelete = () => {
  emit('delete')
}
</script>

<template>
  <div class="type-container" v-if="typeDefinition">
    <el-row justify="space-between">
      <el-col :span="20">
        <span class="type-title">{{ index }}) {{ typeDefinition.title }} ({{ modelValue.key }})</span>
      </el-col>
      <el-col :span="4" style="text-align: right">
        <el-button type="danger" size="small" plain @click="handleDelete">删除</el-button>
      </el-col>
    </el-row>
    <div
      v-if="modelValue.options && modelValue.options.length > 0"
      class="params-section"
    >
      <el-descriptions :column="6" :border="true" size="small">
        <el-descriptions-item
          v-for="item in filledOptions"
          :key="item.option.name"
          :label-width="110"
          :label-align="'right'"
        >
          <template #label>
            <el-tooltip
              :disabled="!item.option.description"
              :content="item.option.description"
              placement="top"
            >
              <span>{{ item.option.title || '' }}</span>
            </el-tooltip>
          </template>
          <template v-if="item.option.title">
            <!-- Number type -->
            <el-input-number
              v-if="item.option.type === 'number'"
              v-model="item.value"
              size="small"
              controls-position="right"
            />
            <!-- Option type -->
            <el-select
              v-else-if="item.option.type === 'option'"
              v-model="item.value"
              placeholder="Select"
              size="small"
            >
              <el-option
                v-for="opt in item.option.options"
                :key="opt"
                :label="opt"
                :value="opt"
              />
            </el-select>
            <!-- String and other types -->
            <el-input
              v-else
              v-model="item.value"
              size="small"
            />
          </template>
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<style scoped>
.type-container {
  padding: 10px;
  /* border: 1px solid #ebeef5; */
  border-radius: 4px;
  margin-bottom: 10px;
}
.type-title {
  font-weight: bold;
  font-size: 12px;
}
.params-section {
  margin-top: 10px;
}
.params-section :deep(.el-select),
.params-section :deep(.el-input-number),
.params-section :deep(.el-input) {
  width: 80px;
}
.params-section :deep(.el-input-number .el-input__inner) {
  text-align: left;
}
</style>