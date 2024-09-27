<script setup lang="ts">
import { ElForm, ElFormItem, ElInput, ElText } from 'element-plus'
import { ref } from 'vue';

interface Data {
  type: number,
  code: string,
  quantity: number,
  expense: number,
  comment?: string,
  created?: Date
}

const form = ref<Data>({
  type: 1,
  code: '',
  quantity: 0,
  expense: 0.0,
  created: new Date()
})

</script>
<template>
  <ElForm v-model="form" label-width="auto">
    <ElFormItem label="代码" required>
      <ElInput v-model="form.code" />
    </ElFormItem>
    <ElFormItem label="名称" required>
      <ElText> ABC </ElText>
    </ElFormItem>    
  </ElForm>
</template>