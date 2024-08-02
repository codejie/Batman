<script setup lang="ts">
import { PropType, defineProps, ref, unref, watch } from 'vue'
import { InstanceModel } from '@/api/strategy/types'
import { ElForm, ElFormItem, ElTable, ElTableColumn, ElRow, ElCol, ElSelect, ElOption, ElButton, ElMessage } from 'element-plus'
import { ReqParam, KLinePanel, ShowParam } from '@/components/KLine'
import { apiCreate } from '@/api/customized';

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
    label: '+0 days'
  },
  {
    value: 14,
    label: '+14 days'
  },
  {
    value: 28,
    label: '+28 days'
  },
  {
    value: 60,
    label: '+60 days'
  }  
]

function getDateString(date: string, days: number): string {
  if (days == 0)
    return date
  const tmp = new Date(Date.parse(date))
  tmp.setDate(tmp.getDate() + days)
  return tmp.toISOString().slice(0, 10)
}

const showParam = ref<ShowParam>({
  maLines: [5, 12, 30 ],
  hideVolume: false,
  markLines: true
})
const reqParam = ref<ReqParam>()
const dateRange = ref<number>(0)
let selectRow: any = ref<any>()

function updateChartParam(days: number) {
  const start = getDateString(props.instance?.result_params.start, -days)
  const end = getDateString(props.instance?.result_params.end, days)

  reqParam.value = {
    code: selectRow.value?.code,
    start: start,
    end: end
  }
}

function onRowClick(row: any) {
  selectRow.value = row
  updateChartParam(unref(dateRange))
}

watch(
  () => dateRange.value,
  (value) => {
    if (selectRow.value)
      updateChartParam(unref(value))
  }
)

async function onCustomizedClick() {
  const ret = await apiCreate({
    code: unref(selectRow).code,
    type: 1
  })
  if (ret.code == 0) {
    ElMessage({
        type: 'success',
        message: `${unref(selectRow).code} added to customized list.`
      })    
  }
}

function onZoomClick() {
  showParam.value = {
    maLines: showParam.value.maLines,
    hideVolume: !showParam.value.hideVolume,
    markLines: true
  }
}

</script>
<template>
  <ElForm label-width="auto">
    <ElFormItem label="Updated">
      {{ instance?.latest_updated }} 
    </ElFormItem>
    <ElFormItem label="Results">
      <ElRow :gutter="24" style="width: 100%">
        <ElCol :span="7">
          <ElTable :data="instance?.results" @row-click="onRowClick" :border="true" height="500" highlight-current-row>
            <ElTableColumn prop="code" label="Code" width="100" />
            <ElTableColumn prop="name" label="Name" width="100" />
            <ElTableColumn prop="date" label="Date" />
          </ElTable>
        </ElCol>
        <ElCol :span="17">
          <ElRow v-if="selectRow" :gutter="24" sytle="width: 100%">
            <ElCol :span="24">
              <div class="bold">
                {{ selectRow?.code }}({{ selectRow?.name }})
                <ElButton size="small" style="margin-left: 12px" @click="onCustomizedClick">Add to Customized</ElButton>
                <ElSelect v-model="dateRange" size="small" style="width: 15%; float: right">
                  <ElOption v-for="item in extRanges" :key="item.value" :label="item.label" :value="item.value" />
                </ElSelect>
                <ElButton size="small" style="margin-left: 12px; float: right; margin-right: 12px;" @click="onZoomClick">Zoom</ElButton>
              </div>
            </ElCol>
          </ElRow>
          <KLinePanel :reqParam="reqParam" :showParam="showParam" />
        </ElCol>
      </ElRow>
    </ElFormItem>
  </ElForm>
</template>
<style lang="css">
.bold {
  font-weight: bold;
}
</style>
