<script setup lang="ts">
import { defineProps, onMounted, ref, unref } from 'vue'
import { InstanceItemModel  } from '@/api/strategy/types'
import { ElForm, ElFormItem, ElTable, ElTableColumn, ElRow, ElCol } from 'element-plus'
import { KLinePanel2, ReqParam } from '@/components/KLine'
import { apiCreate } from '@/api/customized';
import { apiGet } from '@/api/strategy';



const props = defineProps({
  instanceId: {
    type: String,
    required: true
  }
})

const reqParam = ref<ReqParam>()
const initParam = ref({
  maGroup: [7, 9, 12, 17, 26, 30, 45],
  maLines: [7, 12, 26],
  zoom: false,
  volume: true
})

const instance = ref<InstanceItemModel>()

function getDateString(date: string, days: number): string {
  if (days == 0)
    return date
  const tmp = new Date(Date.parse(date))
  tmp.setDate(tmp.getDate() + days)
  return tmp.toISOString().slice(0, 10)
}

const dateRange = ref<number>(0)
let selectRow: any = ref<any>()

function updateChartParam(days: number) {
  const start = getDateString(unref(instance)?.result_params.start, -days)
  const end = getDateString(unref(instance)?.result_params.end, days)

  reqParam.value = {
    code: selectRow.value?.code,
    start: start,
    end: end
  }
}

function makeResultDate(row: any): string {
  if (row.results.length === 1)
    return row.results[0].date
  else
    return `${row.results[0].date}[${row.results.length}]`
}

function onRowClick(row: any) {
  selectRow.value = row
  updateChartParam(unref(dateRange))``
}

onMounted(async () => {
  const retGet = await apiGet({
    id: props.instanceId
  })
  instance.value = retGet.result
})

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
            <ElTableColumn prop="code" label="Code" width="80" />
            <ElTableColumn prop="name" label="Name" width="90" />
            <ElTableColumn prop="date" label="Date">
              <template #default="scope">
                {{ makeResultDate(scope.row) }}
              </template>              
            </ElTableColumn>
          </ElTable>
        </ElCol>
        <ElCol :span="17">
          <KLinePanel2 :req-param="reqParam!" :init-param="initParam" />
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
