<script setup lang="ts">
import { AlgorithmCategoryOptionType, AlgorithmTypeDefinitions } from '@/api/calc/defines'
import {
  ElButton,
  ElRow,
  ElCol,
  ElInput,
  ElDescriptions,
  ElDescriptionsItem
} from 'element-plus'
import { computed, type PropType } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object as PropType<{
        key: number,
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
  }
})

const typeDefinition = computed(() => {
  return AlgorithmTypeDefinitions[props.modelValue.key]
})

const filledOptions = computed(() => {
  const options = props.modelValue.options
  if (!options || options.length === 0) {
    return []
  }
  const filled = [...options]
  const remainder = options.length % 3
  if (remainder > 0) {
    const toAdd = 3 - remainder
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
  <div class="type-container">
    <el-row justify="space-between">
      <el-col :span="20">
        <p>
          <strong>{{ index }}). {{ typeDefinition.title }}</strong> ({{ typeDefinition.name
          }})
        </p>
      </el-col>
      <el-col :span="4" style="text-align: right">
        <el-button type="danger" size="small" plain @click="handleDelete">删除</el-button>
      </el-col>
    </el-row>
    <div
      v-if="modelValue.options && modelValue.options.length > 0"
      class="params-section"
    >
      <el-descriptions :column="3" :border="true" size="small">
        <el-descriptions-item
          v-for="item in filledOptions"
          :key="item.option.name"
          :label="item.option.title || ''"
        >
          <el-input v-if="item.option.title" v-model="item.value" size="small" />
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<style scoped>
.type-container {
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 10px;
}
.params-section {
  margin-top: 10px;
}
</style>