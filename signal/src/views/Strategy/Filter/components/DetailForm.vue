<script setup lang="ts">
import { defineProps, onMounted, ref, unref, watch } from 'vue'
import { InstanceItemModel, InstanceItemResult, StrategyModel, TriggerModel } from '@/api/strategy/types'
import { ElRow, ElCol, ElTable, ElTableColumn, ElRadioGroup, ElRadioButton } from 'element-plus'
import { apiGet, apiInfos } from '@/api/strategy';
import { apiInfos as algo_apiInfos } from '@/api/algorithm'
import { AlgorithmModel } from '@/api/algorithm/types';

type Argument = {
  label: string,
  value: string,
  desc?: string
}

const props = defineProps({
  instanceId: {
    type: String,
    required: true
  }
})

const instance = ref<InstanceItemModel>()
const strategy = ref<StrategyModel>()
const strategyArgs = ref<Argument[]>([])
const strategyState = ref<string>('-')
const strategyTrigger = ref<string>('-')
const resultUpdated = ref<string>('-')
const results = ref<any[]>([])

const algorithm = ref()
const algorithm_desc = ref<string>()
const algorithmArgs = ref<Argument[]>([])

function makeTrigger(trigger?: TriggerModel): string {
  if (trigger) {
    if (trigger.mode == 'daily') {
      return `(每日)${trigger.hour}:${trigger.minute}`
    } else if (trigger.mode == 'delay') {
      return `(延迟)${trigger.seconds}秒`
    } else {
      return 'unknown'
    }
    return `(${trigger!.mode})`
  } else {
    return '-'
  }
}

function makeUpdated(updated?: Date): string {
  const date = new Date(updated || 0)
  return `${date.toISOString().slice(0, 10)} ${date.toISOString().slice(11, 19)}`
}

function makeState(is_removed?: boolean, state?: number): string {
  if (is_removed) {
    return 'Removed'
  }
  switch(state) {
    case 0:
      return 'Init'
    case 1:
      return 'Ready'
    case 2:
      return 'Executed'
    case 3:
      return 'Error'
    case 4:
      return 'Missed'
    case 5:
      return 'Removed'
    case 6:
      return 'Paused'
    default:
      return 'Unknown'
  }
}

function makeStrategyArgs(args?: any[], values?: any): Argument[] {
  const ret:Argument[] = []
  if (args && values) {
    args.forEach(item => {
      ret.push({
        label: item.name,
        value: values[item.name] + (item.unit || ''),
        desc: item.desc
      })
    })
  }
  return ret
}

async function onAlgorithmChange(value: string) {
  const ret = await algo_apiInfos({
    name: value
  })
  const algo = ret.result as AlgorithmModel
  algorithm_desc.value = algo.desc

  const s_algo = unref(instance)?.algo_values![value]
  algorithmArgs.value = []
  algo.args?.forEach(item => {
    algorithmArgs.value.push({
      label: item.name,
      value: s_algo ? s_algo[item.name] + (item.unit || '') : '',
      desc: item.desc
    })
  })
}


function makeResults(results?: InstanceItemResult[]) {
  const ret: any[] = []
  if (results) {
    for (const r of results) {
      ret.push({
        code: r.code,
        name: r.name,
        date: r.results[0].date
      })
    }
  }
  return ret
}

onMounted(async () => {
  const retGet = await apiGet({
    id: props.instanceId
  })
  instance.value = retGet.result

  const retStg = await apiInfos({
    id: unref(instance)?.strategy
  })
  
  strategy.value = retStg.result[0]
  await onAlgorithmChange(unref(strategy)!.algorithms![0])
})

watch(
  instance,
  () => {
    strategyState.value = makeState(unref(instance)?.is_removed, unref(instance)?.state)
    strategyTrigger.value = makeTrigger(unref(instance)?.trigger)
    resultUpdated.value = makeUpdated(unref(instance)?.latest_updated)
    results.value = makeResults(unref(instance)?.results)
  }
)

watch(
  strategy,
  () => {
    strategyArgs.value = makeStrategyArgs(unref(strategy)?.args, unref(instance)?.arg_values)
  }
)

</script>
<template>
  <ElRow :gutter="24">
    <ElCol :span="14">
      <ElRow class="row" :gutter="24">
        <ElCol :span="4">策略</ElCol>
        <ElCol :span="20">{{ strategy?.name }}</ElCol>
      </ElRow>       
      <ElRow class="row" :gutter="24">
        <ElCol :span="4" />
        <ElCol :span="20">{{ strategy?.desc }}</ElCol>
      </ElRow>       
      <ElRow class="row" :gutter="24">
        <ElCol :span="24">Strategy Arguments</ElCol>
      </ElRow>      
      <ElRow class="row" :gutter="24">
        <ElCol :span="2" />
        <ElCol :span="22">
          <ElTable :data="strategyArgs" :border="true">
            <ElTableColumn prop="label" label="Item" width="120" />
            <ElTableColumn prop="value" label="Value" width="100" />
            <ElTableColumn prop="desc" label="Desc" />
          </ElTable>
        </ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="24">Algorithm Arguments</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="2" />
        <ElCol :span="22">
          <div class="row">
            <ElRadioGroup v-model="algorithm" @change="onAlgorithmChange">
              <ElRadioButton size="small" v-for="item in strategy?.algorithms" :key="item" :label="item" :value="item" />
            </ElRadioGroup>
          </div>
          <div class="row">{{ algorithm_desc }}</div>
          <div class="row">
            <ElTable :data="algorithmArgs" :border="true">
              <ElTableColumn prop="label" label="Item" width="120" />
              <ElTableColumn prop="value" label="Value" width="100" />
              <ElTableColumn prop="desc" label="Desc" />
            </ElTable>
          </div>
        </ElCol>
      </ElRow>           
    </ElCol>
    <ElCol :span="1" />
    <ElCol :span="9">
      <ElRow class="row" :gutter="24">
        <ElCol :span="6">状态</ElCol>
        <ElCol :span="18">{{ strategyState }}</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="6">定时器</ElCol>
        <ElCol :span="18">{{ strategyTrigger }}</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="6">Updated</ElCol>
        <ElCol :span="18">{{ resultUpdated }}</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="24">Result ({{ results.length }})</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="24">
          <ElTable :data="results" :border="true" max-height="440">
            <ElTableColumn prop="code" label="Code" width="80" />
            <ElTableColumn prop="name" label="Name" width="90" />
            <ElTableColumn prop="date" label="Date" />             
          </ElTable>
        </ElCol>        
      </ElRow>
    </ElCol>    
  </ElRow>
</template>
<style lang="css">
.row {
  margin-top: 4px;
  margin-bottom: 4px;
}
</style>
