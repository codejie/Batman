<script setup lang="ts">
import { ref } from 'vue'
import { ElCard, ElForm, ElFormItem, ElInput, ElButton, ElMessageBox } from 'element-plus'
import type { PropType } from 'vue'

// Define a more specific type for the modelValue prop
interface AlgorithmType {
  name: string
  title: string
  description: string
}

const props = defineProps({
  modelValue: {
    type: Object as PropType<AlgorithmType>,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'delete'])

const isEditing = ref(false)
const editableValue = ref<AlgorithmType>({ ...props.modelValue })

const handleEdit = () => {
  isEditing.value = true
  editableValue.value = { ...props.modelValue }
}

const handleSave = () => {
  emit('update:modelValue', editableValue.value)
  isEditing.value = false
}

const handleCancel = () => {
  isEditing.value = false
}

const handleDelete = () => {
  ElMessageBox.confirm('此操作将永久删除该算法类型, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      emit('delete')
    })
    .catch(() => {
      // catch cancel
    })
}
</script>

<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>{{ modelValue.title }}</span>
        <div>
          <el-button v-if="!isEditing" class="button" type="primary" text @click="handleEdit">编辑</el-button>
          <el-button v-if="isEditing" class="button" type="primary" text @click="handleSave">保存</el-button>
          <el-button v-if="isEditing" class="button" text @click="handleCancel">取消</el-button>
          <el-button class="button" type="danger" text @click="handleDelete">删除</el-button>
        </div>
      </div>
    </template>
    <div v-if="!isEditing">
      <div><strong>名称:</strong> {{ modelValue.name }}</div>
      <div><strong>描述:</strong> {{ modelValue.description }}</div>
    </div>
    <el-form v-else :model="editableValue" label-position="top">
      <el-form-item label="标题">
        <el-input v-model="editableValue.title" />
      </el-form-item>
      <el-form-item label="名称">
        <el-input v-model="editableValue.name" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="editableValue.description" type="textarea" />
      </el-form-item>
    </el-form>
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
