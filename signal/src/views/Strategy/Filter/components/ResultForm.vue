<script setup lang="ts">
import { PropType, defineProps, ref, unref, watch } from 'vue'
import { InstanceModel } from '@/api/strategy/types'
import { ElForm, ElFormItem, ElTable, ElTableColumn, ElRow, ElCol, ElSelect, ElOption, ElButton, ElMessage } from 'element-plus'
// import KLinePanel, { Param } from '@/views/Strategy/components/KLinePanel.vue'
import KLinePanel, { DataParam, ShowParam } from '@/components/KLine/src/KLinePanel.vue';
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
    label: 'current'
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
  maLines: [5, 10, 12, 24]
})
const dataParam = ref<DataParam>()
const dateRange = ref<number>(0)
let selectRow: any = ref<any>()

function updateChartParam(days: number) {
  const start = getDateString(props.instance?.result_params.start, -days)
  const end = getDateString(props.instance?.result_params.end, days)

  dataParam.value = {
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
            <ElCol :span="12">
              <div class="bold">
                {{ selectRow?.code }}({{ selectRow?.name }})
                <ElButton size="small" style="margin-left: 12px" @click="onCustomizedClick">Add to Customized</ElButton>
              </div>
            </ElCol>
            <ElCol :span="6">
              <ElButton size="small" style="float: left">Add to Customized</ElButton>
              <!-- <ElButton size="small" style="float: right; margin-right: 12px">{{ selectRow?.name }}</ElButton> -->
            </ElCol>
            <ElCol :span="6">
              <ElSelect v-model="dateRange" size="small" style="width: 80%; float: right">
                <ElOption v-for="item in extRanges" :key="item.value" :label="item.label" :value="item.value" />
              </ElSelect>
            </ElCol>
          </ElRow>
          <KLinePanel :data="dataParam" :show="showParam" />
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
