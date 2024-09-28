<script setup lang="ts">
import { apiInfo } from '@/api/data/wrap';
import { ElDatePicker, ElForm, ElFormItem, ElInput, ElText } from 'element-plus'
import { ref, watch } from 'vue';

interface Data {
  type: number,
  code: string,
  quantity: number,
  expense: number,
  comment?: string,
  created: Date
}

const form = ref<Data>({
  type: 1,
  code: '',
  quantity: 0,
  expense: 0.0,
  created: new Date()
})

const name = ref<string>('')

defineExpose({
  form: form.value
})

function disableDate(date: Date) {
  return date.getDay() === 0 || date.getDay() === 6
}

async function fetchCodeName(type: number, code: string) {
  const ret = await apiInfo(
    {
      code: code
    },
    type)

  if (ret.result) {
    name.value = ret.result.name
  }
}

let searchTimer: NodeJS.Timeout
watch(
  () => form.value.code,
  async () => {
    if (!form.value.code || form.value.code.length < 6) {
      name.value = ''
      return
    }

    clearTimeout(searchTimer)
    searchTimer = setTimeout(async () => {
      await fetchCodeName(form.value.type, form.value.code)
    }, 150)
  }
)

</script>
<template>
  <ElForm v-model="form" label-width="auto">
    <ElFormItem label="代码" required>
      <ElInput v-model="form.code" type="string" :clearable="true" maxlength="6" />
    </ElFormItem>
    <ElFormItem label="名称">
      <ElText> {{ name }} </ElText>
    </ElFormItem>
    <ElFormItem label="数量" type="number" required>
      <ElInput v-model="form.quantity" :clearable="true" />
    </ElFormItem>
    <ElFormItem label="费用" type="number" required>
      <ElInput v-model="form.expense" :clearable="true" />
    </ElFormItem>
    <ElFormItem label="日期" required>
      <ElDatePicker v-model="form.created" type="date" :disabled-date="disableDate" />
    </ElFormItem>
    <ElFormItem label="备注">
      <ElInput v-model="form.comment" :clearable="true" />
    </ElFormItem>  
  </ElForm>
</template>