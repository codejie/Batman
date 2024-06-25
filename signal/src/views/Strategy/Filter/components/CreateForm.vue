<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElForm, ElFormItem, ElInput, ElOption, ElSelect, ElTable, ElText } from 'element-plus'
import { apiInfos } from '@/api/strategy'
import { StrategyModel } from '@/api/strategy/types'

const strategyList = ref<StrategyModel[]>([])
const getStrategyList = async () => {
  const ret = await apiInfos({})
  strategyList.value = ret.result
}

const form1 = ref<any>({
  name: '',
  strategy: ''
})

onMounted(() => {
  getStrategyList()
})
</script>
<template>
  <ElInput v-model="text" />
  <ElForm :model="form1" label-width="auto">
    <ElFormItem label="Name" required>
      <ElInput :model="form1.name" />
    </ElFormItem>
    <ElFormItem label="Strategy" required>
      <ElSelect :model="form1.strategy" placeholder="select a strategy">
        <ElOption v-for="item in strategyList" :key="item.id" :label="item.name" :value="item.id" />
      </ElSelect>
    </ElFormItem>
    <ElFormItem v-if="form1.strategy !== ''" label="Strategy Arguments">
      <ElTable />
    </ElFormItem>
    <ElFormItem label="Strategy Algorithms">
      <ElText>algorithm</ElText>
    </ElFormItem>
  </ElForm>
</template>
