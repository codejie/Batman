<script setup lang="ts">
import { onMounted, ref, unref, watch } from 'vue'
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElOption,
  ElSelect,
  ElTable,
  ElTableColumn,
  ElText
} from 'element-plus'
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
    for (let i = 0; i < value.args.length; ++i) {
      value.args[i]['arg_value'] = undefined
    }
    return value
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
        <ElOption v-for="s in strategyList" :key="s.id" :label="s.name" :value="s" />
      </ElSelect>
    </ElFormItem>
    <div v-if="form.strategy">
      <ElFormItem label="Strategy Description">
        <ElText>{{ form.strategy.desc }}</ElText>
      </ElFormItem>
      <ElFormItem label="Strategy Arguments">
        <ElTable :data="form.strategy.args" border style="width: 100%">
          <ElTableColumn prop="name" label="Name" width="100" />
          <ElTableColumn prop="unit" label="Unit" width="100" />
          <ElTableColumn prop="arg_values" label="Value" width="150">
            <template v-slot="{ row }">
              {{ row }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="desc" label="desc" width="100" />
        </ElTable>
      </ElFormItem>
      <ElFormItem label="Strategy Algorithms">
        <ElText>{{ form.strategy }}</ElText>
        <div v-for="a in form.strategy.algorithms" :key="a">
          <ElText>{{ a }}</ElText>
          <!-- <ElForm v-for="item in form.strategy.algorithms" :key="item.name">
            <ElFormItem>
              <ElInput />
            </ElFormItem>
          </ElForm> -->
        </div>
      </ElFormItem>
    </div>
  </ElForm>
</template>
