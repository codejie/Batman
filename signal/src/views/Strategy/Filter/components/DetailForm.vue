<script setup lang="ts">
import { defineProps, onMounted, ref, unref } from 'vue'
import { InstanceItemModel, StrategyModel } from '@/api/strategy/types'
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
const algorithm = ref()
const algorithm_desc = ref<string>()
const algorithmArgs = ref<Argument[]>([])

function makeTrigger(): string {
  if (instance.value) {
    const trigger = unref(instance)!.trigger
    if (trigger.mode == 'daily') {
      return `(每日)${trigger.hour}:${trigger.minute}`
    } else if (trigger.mode == 'delay') {
      return `(延迟)${trigger.seconds}秒`
    } else {
      return 'unknown'
    }
    return `(${trigger.mode})`
  }
  return '-'
}

function makeUpdated(): string {
  const date = new Date(unref(instance)!.latest_updated || 0)
  return `${date.toISOString().slice(0, 10)} ${date.toISOString().slice(11, 19)}`
}

function makeState(): string {
  if (unref(instance)?.is_removed) {
    return 'Removed'
  }
  switch(unref(instance)?.state) {
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

function makeStrategyArgs(): Argument[] {
  const ret:Argument[] = []
  strategy.value?.args?.forEach(item => {
    ret.push({
      label: item.name,
      value: unref(instance)?.arg_values?.[item.name] + (item.unit || ''),
      desc: item.desc
    })
  })
  return ret
}

async function onAlgorithmChange(value: string) {
  const ret = await algo_apiInfos({
    name: value
  })
  const algo = ret.result as AlgorithmModel
  console.log(algo)
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

function makeResultDate(row: any): string {
  const result = row.results[0]
  return result.date
}

onMounted(async () => {
  console.log(props.instanceId)
  const retGet = await apiGet({
    id: props.instanceId
  })
  instance.value = retGet.result
  console.log(unref(instance)?.strategy)

  const retStg = await apiInfos({
    id: unref(instance)?.strategy
  })
  
  strategy.value = retStg.result[0]
  console.log(strategy.value)
  await onAlgorithmChange(unref(strategy)!.algorithms![0])

})

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
          <ElTable :data="makeStrategyArgs()" :border="true">
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
        <ElCol :span="18">{{ makeState() }}</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="6">定时器</ElCol>
        <ElCol :span="18">{{ makeTrigger() }}</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="6">Updated</ElCol>
        <ElCol :span="18">{{ makeUpdated() }}</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="24">Result ({{ instance?.results?.length }})</ElCol>
      </ElRow>
      <ElRow class="row" :gutter="24">
        <ElCol :span="24">
          <ElTable :data="instance?.results" :border="true" max-height="440">
            <ElTableColumn prop="code" label="Code" width="80" />
            <ElTableColumn prop="name" label="Name" width="90" />
            <ElTableColumn prop="date" label="Date">
              <template #default="scope">
                {{ makeResultDate(scope.row) }}
              </template>              
            </ElTableColumn>
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
