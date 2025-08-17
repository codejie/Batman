<script setup lang="ts">
import { ElRow, ElCol, ElDivider } from 'element-plus'
import { computed, type PropType } from 'vue'
import { AlgorithmCategoryDefinitions, AlgorithmCategoryOptionType } from '@/api/calc/defines'
import AlgorithmType from './AlgorithmType.vue'

const props = defineProps({
  categoryKey: {
    type: Number,
    required: true
  },
  types: {
    type: Array as PropType<Array<{
        key: number,
        options: Array<{
          option: AlgorithmCategoryOptionType,
          value?: any  
        }>
    }>>,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['delete-type', 'update-type-params'])

const category = computed(() => {
  return AlgorithmCategoryDefinitions[props.categoryKey]
})

// const typesWithDefs = computed(() => {
//   return props.types.map((t) => {
//     console.log(t)
//     return {
//       ...t,
//       definition: AlgorithmTypeDefinitions[t.key]
//     }
//   })
// })

const handleDeleteType = (typeKeyToDelete: number) => {
  emit('delete-type', { categoryKey: props.categoryKey, typeKey: typeKeyToDelete })
}

// const handleUpdateParams = (typeKey: number, params: any) => {
//   emit('update-type-params', { categoryKey: props.categoryKey, typeKey, params })
// }
</script>

<template>
  <div class="category-container">
    <div class="category-header">
      <span class="category-title">{{ index }}. {{ category.title }}</span>
      <span class="category-name">({{ category.name }})</span>:
      <span class="category-description">{{ category.description }}</span>
    </div>

    <el-divider />

    <el-row :gutter="20" class="type-list">
      <el-col :span="24" v-for="(type, typeIndex) in types" :key="type.key">
        <AlgorithmType
          :model-value="type"
          :index="typeIndex + 1"
          @delete="handleDeleteType(type.key)"
        />
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.category-container {
  margin-bottom: 20px;
}
.category-header {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}
.type-list {
  margin-left: 20px;
}
</style>
