<script setup lang="ts">
import { PropType, defineProps, ref, unref } from 'vue'
import { InstanceModel } from '@/api/strategy/types'
import { ElForm, ElFormItem, ElTable, ElTableColumn, ElRow, ElCol } from 'element-plus'
import KLinePanel, { Param } from '@/views/Strategy/components/KLinePanel.vue'

defineProps({
  instance: {
    type: Object as PropType<InstanceModel>
  }
})

const chartParam = ref<Param>()
const selected = ref(false)
function onRowClick(row: any) {
  console.log(row)
  selected.value = true
  chartParam.value = {
    code: row.code,
    start: '2023-10-01',
    end: '2024-01-01'
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
        <ElCol :span="10">
          <ElTable :data="instance?.results" @row-click="onRowClick" border height="500">
            <ElTableColumn prop="code" label="Code" width="100" />
            <ElTableColumn prop="name" label="Name" width="100" />
            <ElTableColumn prop="date" label="Date" />
          </ElTable>
        </ElCol>
        <ElCol :span="14">
          <KLinePanel v-if="selected" :param="chartParam" />
        </ElCol>
      </ElRow>
    </ElFormItem>
  </ElForm>
</template>
