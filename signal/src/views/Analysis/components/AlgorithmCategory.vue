<script setup lang="ts">
import { ElRow, ElCol, ElDivider } from 'element-plus'
import { computed, type PropType } from 'vue'
import AlgorithmType from './AlgorithmType.vue'
import { AlgorithmCategoryDefinitions, AlgorithmTypeOptionType } from '@/api/calc/defines'

// Define specific types for props
// interface AlgorithmTypeItem {
//   category: number
//   name: string
//   title: string
//   description: string
// }

// interface AlgorithmCategoryItem {
//   name: string
//   title: string
//   description: string
//   options: any[] // Keeping options flexible for now
// }

const props = defineProps({
  categoryKey: {
    type: Number, //Object as PropType<AlgorithmCategoryItem>,
    required: true
  },
  types: {
    type: Array as PropType<AlgorithmTypeOptionType[]>,
    required: true
  },
  categoryId: {
    type: Number,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
})

const category = computed(() => {
  return AlgorithmCategoryDefinitions[props.categoryKey]
})

// const type = 
</script>

<template>
  <div class="category-container">
    <div class="category-header">
      <span class="category-title">{{ index }}. {{ category.title }}</span>
      <span class="category-name">({{ category.name }})</span>:
      <span class="category-description">{{ category.description }}</span>
    </div>

    <el-divider />

    <!-- <el-row :gutter="20" class="type-list">
      <el-col :span="8" v-for="type in types" :key="type.name">
        <AlgorithmType :model-value="type" />
      </el-col>
    </el-row> -->
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