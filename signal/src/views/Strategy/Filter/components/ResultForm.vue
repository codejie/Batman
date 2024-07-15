<script setup lang="ts">
import { PropType, defineProps, ref, unref, watch } from 'vue'
import { InstanceModel } from '@/api/strategy/types'
import { ElForm, ElFormItem, ElTable, ElTableColumn, ElRow, ElCol, ElSelect, ElOption } from 'element-plus'
import KLinePanel, { Param } from '@/views/Strategy/components/KLinePanel.vue'

const props = defineProps({
  instance: {
    type: Object as PropType<InstanceModel>
  }
})

const extRanges = [
  // {
  //   value: -14,
  //   label: '-14days'
  // },  
  {
    value: 0,
    label: 'current'
  },
  {
    value: 14,
    label: '+14days'
  },
  {
    value: 28,
    label: '+28days'
  },
  {
    value: 60,
    label: '+60days'
  }  
]

function getDateString(date: string, days: number): string {
  if (days == 0)
    return date
  const tmp = new Date(Date.parse(date))
  tmp.setDate(tmp.getDate() + days)
  return tmp.toISOString().slice(0, 10)
}

const chartParam = ref<Param>()
const dateRange = ref<number>(0)
let selectCode = undefined

function updateChartParam(days: number) {
  const start = getDateString(props.instance?.result_params.start, -days)
  const end = getDateString(props.instance?.result_params.end, days)

  chartParam.value = {
    code: selectCode!,
    start: start,
    end: end
  }
}

function onRowClick(row: any) {
  selectCode = row.code
  updateChartParam(unref(dateRange))
}

watch(
  () => dateRange.value,
  (value) => {
    if (selectCode)
      updateChartParam(unref(value))
  }
)

</script>
<template>
  <ElForm label-width="auto">
    <ElFormItem label="Updated">
      {{ instance?.latest_updated }} 
    </ElFormItem>
    <ElFormItem label="Results">
      <ElRow :gutter="24" style="width: 100%">
        <ElCol :span="8">
          <ElTable :data="instance?.results" @row-click="onRowClick" border height="500">
            <ElTableColumn prop="code" label="Code" width="100" />
            <ElTableColumn prop="name" label="Name" width="100" />
            <ElTableColumn prop="date" label="Date" />
          </ElTable>
        </ElCol>
        <ElCol :span="16">
          <ElSelect v-model="dateRange" size="small" style="width: 30%">
            <ElOption v-for="item in extRanges" :key="item.value" :label="item.label" :value="item.value" />
          </ElSelect>
          <KLinePanel :param="chartParam" />
        </ElCol>
      </ElRow>
    </ElFormItem>
  </ElForm>
</template>
