<script setup lang="ts">
import { onMounted, reactive, ref, unref, watch } from 'vue'
import { ElForm, ElFormItem, ElInput, ElOption, ElSelect, ElTable, ElText } from 'element-plus'
import { apiInfos } from '@/api/strategy'
import { StrategyModel } from '@/api/strategy/types'

const strategyList = ref<StrategyModel[]>([])
const form = ref<any>({
  name: '',
  strategy: undefined
})
// const algorithm = ref<>()

const getStrategyList = async () => {
  const ret = await apiInfos({})
  strategyList.value = ret.result
}
// const getAlgorithm = async() => {
// }

onMounted(() => {
  getStrategyList()
})

watch(
  () => unref(form).strategy,
  (value) => {
    console.log(value)
  }
)
</script>
<template>
  <ElForm v-model="form" label-width="auto">
    <ElFormItem label="Name" required>
      <ElInput v-model="form.name" />
    </ElFormItem>
    <ElFormItem label="Strategy" required>
      <ElSelect v-model="form.strategy" placeholder="select a strategy">
        <ElOption v-for="item in strategyList" :key="item.id" :label="item.name" :value="item" />
      </ElSelect>
    </ElFormItem>
    <div v-if="form.strategy">
      <ElFormItem label="Strategy Description">
        <ElText>{{ form.strategy.desc }}</ElText>
      </ElFormItem>
      <ElFormItem label="Strategy Arguments">
        <ElTable />
      </ElFormItem>
      <ElFormItem label="Strategy Algorithms">
        <ElText>{{ form.strategy }}</ElText>
        <div v-for="item in form.strategy.algorithms" :key="item">
          <ElText>{{ item }}</ElText>
          <ElForm v-for="item in form.strategy.algorithms" :key="item.name">
            <ElFormItem>
              <ElInput />
            </ElFormItem>
          </ElForm>
        </div>
      </ElFormItem>
    </div>
  </ElForm>
</template>
