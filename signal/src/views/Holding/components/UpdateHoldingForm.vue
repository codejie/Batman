<script setup lang="ts">
import { ReqParam } from '@/components/KLine';
import { ElDatePicker, ElForm, ElFormItem, ElInput, ElRadioGroup, ElText, ElRadio } from 'element-plus'
import { PropType, ref } from 'vue';

const props = defineProps({
  reqParam: {
    type: Object as PropType<ReqParam>,
    required: true
  }
})

interface Data {
  type: number,
  code: string,
  name: string,
  action: number,
  quantity: number,
  expense: number,
  comment?: string,
  created: Date
}

const form = ref<Data>({
  type: props.reqParam.type,
  code: props.reqParam.code,
  name: props.reqParam.name!,
  action: 0,
  quantity: 0,
  expense: 0.0,
  created: new Date()
})

defineExpose({
  form: form.value
})

function disableDate(date: Date) {
  return date.getDay() === 0 || date.getDay() === 6
}

</script>
<template>
  <ElForm v-model="form" label-width="auto">
    <ElFormItem label="代码" required>
      <ElText> {{ form.code }}</ElText>
    </ElFormItem>
    <ElFormItem label="名称">
      <ElText> {{ form.name }} </ElText>
    </ElFormItem>
    <ElFormItem label="操作" required>
      <ElRadioGroup v-model="form.action">
        <ElRadio value="0" label="买入" />
        <ElRadio value="1" label="卖出" />
      </ElRadioGroup>
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