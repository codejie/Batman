<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElForm, ElFormItem, ElInput, ElOption, ElSelect } from 'element-plus'
import { apiInfos } from '@/api/strategy'
import { StrategyModel } from '@/api/strategy/types'
import ArgumentForm from '@/views/Strategy/components/ArgumentForm.vue'
import ResultForm from '@/views/Strategy/components/ResultForm.vue'
import AlgorithmForm from '@/views/Strategy/components/AlgorithmForm.vue'
import TriggerForm from '@/views/Strategy/components/TriggerForm.vue'

const strategyList = ref<StrategyModel[]>([])

interface Props {
  name: string
  strategy?: StrategyModel
}

const form = ref<Props>({
  name: '',
  strategy: undefined
})

const getStrategyList = async () => {
  const ret = await apiInfos({})
  strategyList.value = ret.result
}

onMounted(() => {
  getStrategyList()
})

const result = ref<any>(null)
const argument = ref<any>(null)
const algorithms = ref<any>(null)
const trigger = ref<any>(null)
defineExpose({
  form,
  result,
  argument,
  algorithms,
  trigger
})
</script>
<template>
  <ElForm v-model="form" label-width="auto">
    <ElFormItem label="名称" required>
      <ElInput v-model="form.name" />
    </ElFormItem>
    <ElFormItem label="策略" required>
      <ElSelect v-model="form.strategy" placeholder="选择策略..">
        <ElOption v-for="s in strategyList" :key="s.id" :label="s.name" :value="s" />
      </ElSelect>
    </ElFormItem>
    <!-- <ElFormItem label="temp">
      {{ form.strategy }}
    </ElFormItem> -->
    <div v-if="form.strategy">
      <ElFormItem label="策略结果">
        <ResultForm ref="result" :results="form.strategy.result_fields" />
      </ElFormItem>
      <ElFormItem label="策略参数">
        <ArgumentForm ref="argument" :args="form.strategy.args" />
      </ElFormItem>
      <ElFormItem label="策略算法">
        <AlgorithmForm
          ref="algorithms"
          v-for="item in form.strategy.algorithms"
          :name="item"
          :key="item"
        />
      </ElFormItem>
    </div>
    <ElFormItem label="定时参数">
      <TriggerForm ref="trigger" />
    </ElFormItem>
  </ElForm>
</template>
