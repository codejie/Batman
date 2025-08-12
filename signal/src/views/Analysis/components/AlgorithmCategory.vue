<script setup lang="ts">
import { ref } from 'vue'
import { ElCard, ElForm, ElFormItem, ElInput, ElButton, ElRow, ElCol, ElMessageBox, ElDivider } from 'element-plus'
import type { PropType } from 'vue'
import AlgorithmType from './AlgorithmType.vue'

// Define specific types for props
interface AlgorithmTypeItem {
  category: number
  name: string
  title: string
  description: string
}

interface AlgorithmCategoryItem {
  name: string
  title: string
  description: string
  options: any[] // Keeping options flexible for now
}

const props = defineProps({
  category: {
    type: Object as PropType<AlgorithmCategoryItem>,
    required: true
  },
  types: {
    type: Array as PropType<AlgorithmTypeItem[]>,
    required: true
  },
  categoryId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:category', 'update:types', 'delete:category', 'add:type'])

const isEditing = ref(false)
const editableCategory = ref<AlgorithmCategoryItem>({ ...props.category })

const handleEdit = () => {
  isEditing.value = true
  editableCategory.value = JSON.parse(JSON.stringify(props.category))
}

const handleSave = () => {
  emit('update:category', editableCategory.value)
  isEditing.value = false
}

const handleCancel = () => {
  isEditing.value = false
}

const handleDelete = () => {
  ElMessageBox.confirm('此操作将永久删除该算法分类及其下所有类型, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      emit('delete:category')
    })
    .catch(() => {
      // catch cancel
    })
}

const handleAddType = () => {
  emit('add:type')
}

const handleUpdateType = (updatedType: AlgorithmTypeItem, index: number) => {
  const newTypes = [...props.types]
  newTypes[index] = updatedType
  emit('update:types', newTypes)
}

const handleDeleteType = (index: number) => {
  const newTypes = [...props.types]
  newTypes.splice(index, 1)
  emit('update:types', newTypes)
}
</script>

<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>{{ category.title }}</span>
        <div>
          <el-button v-if="!isEditing" class="button" type="primary" text @click="handleEdit">编辑分类</el-button>
          <el-button v-if="isEditing" class="button" type="primary" text @click="handleSave">保存分类</el-button>
          <el-button v-if="isEditing" class="button" text @click="handleCancel">取消</el-button>
          <el-button class="button" type="danger" text @click="handleDelete">删除分类</el-button>
        </div>
      </div>
    </template>
    <div v-if="!isEditing">
      <div><strong>名称:</strong> {{ category.name }}</div>
      <div><strong>描述:</strong> {{ category.description }}</div>
    </div>
    <el-form v-else :model="editableCategory" label-position="top">
      <el-form-item label="标题">
        <el-input v-model="editableCategory.title" />
      </el-form-item>
      <el-form-item label="名称">
        <el-input v-model="editableCategory.name" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="editableCategory.description" type="textarea" />
      </el-form-item>
    </el-form>

    <el-divider />

    <h3>算法类型</h3>
    <el-row :gutter="20">
      <el-col :span="8" v-for="(type, index) in types" :key="index">
        <AlgorithmType
          :model-value="type"
          @update:model-value="handleUpdateType($event, index)"
          @delete="handleDeleteType(index)"
        />
      </el-col>
    </el-row>
    <el-button type="primary" @click="handleAddType" style="margin-top: 20px;">添加算法类型</el-button>
  </el-card>
</template>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-card {
  margin-bottom: 20px;
}
</style>
