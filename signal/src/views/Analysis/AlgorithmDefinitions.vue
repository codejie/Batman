<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElButton } from 'element-plus'
import AlgorithmCategory from './components/AlgorithmCategory.vue'
import { AlgorithmCategoryDefinitions, AlgorithmTypeDefinitions } from '@/api/calc/defines'

// Make the definitions reactive
const categories = ref(JSON.parse(JSON.stringify(AlgorithmCategoryDefinitions)))
const types = ref(JSON.parse(JSON.stringify(AlgorithmTypeDefinitions)))

const typesByCategory = computed(() => {
  const result: { [key: number]: any[] } = {}
  for (const key in types.value) {
    const type = types.value[key]
    if (!result[type.category]) {
      result[type.category] = []
    }
    result[type.category].push({ ...type, id: key }) // also add original key
  }
  return result
})

const handleUpdateCategory = (updatedCategory: any, categoryId: number) => {
  categories.value[categoryId] = updatedCategory
  ElMessage.success('分类已更新')
  // Here you would typically call an API to save the changes
}

const handleDeleteCategory = (categoryId: number) => {
  // Also delete associated types
  const newTypes = { ...types.value }
  for (const key in newTypes) {
    if (newTypes[key].category === categoryId) {
      delete newTypes[key]
    }
  }
  types.value = newTypes
  delete categories.value[categoryId]
  ElMessage.success('分类已删除')
}

const handleAddType = (categoryId: number) => {
    let maxId = Math.max(...Object.keys(types.value).map(k => parseInt(k, 10)).filter(k => !isNaN(k)), 0)
    const newType = {
        id: maxId + 1,
        category: categoryId,
        name: 'NEW_TYPE',
        title: '新算法类型',
        description: '这是一个新的算法类型'
    }
    types.value[newType.id] = newType;
    ElMessage.success('新类型已添加')
}

const handleUpdateTypes = (updatedTypes: any[], categoryId: number) => {
    const newTypes = { ...types.value };
    // Remove old types for this category
    Object.keys(newTypes).forEach(key => {
        if (newTypes[key].category === categoryId) {
            delete newTypes[key];
        }
    });

    // Add the updated types back
    updatedTypes.forEach(type => {
        newTypes[type.id] = type;
    });

    types.value = newTypes;
    ElMessage.success('类型已更新');
}


const saveChanges = () => {
    // Here you would format the `categories` and `types` objects
    // and send them to your backend to be saved as a file or in a database.
    console.log('Saving categories:', categories.value)
    console.log('Saving types:', types.value)
    ElMessage.success('更改已保存到控制台！')
}

</script>

<template>
  <div>
    <div style="margin-bottom: 20px; display: flex; justify-content: flex-end;">
        <el-button type="primary" @click="saveChanges">保存所有更改</el-button>
    </div>
    <div v-for="(category, categoryId) in categories" :key="categoryId">
      <AlgorithmCategory
        :category="category"
        :types="typesByCategory[categoryId] || []"
        :category-id="Number(categoryId)"
        @update:category="handleUpdateCategory($event, Number(categoryId))"
        @delete:category="handleDeleteCategory(Number(categoryId))"
        @update:types="handleUpdateTypes($event, Number(categoryId))"
        @add:type="handleAddType(Number(categoryId))"
      />
    </div>
  </div>
</template>

<style scoped>
</style>
