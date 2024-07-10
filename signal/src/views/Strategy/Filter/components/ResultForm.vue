<script setup lang="ts">
import { PropType, defineProps } from 'vue'
import { InstanceModel } from '@/api/strategy/types'
import { ElForm, ElFormItem, ElTable, ElTableColumn, ElRow, ElCol } from 'element-plus'


const props = defineProps({
  instance: {
    type: Object as PropType<InstanceModel>
  }
})
</script>
<template>
  <ElForm label-width="auto">
    <ElFormItem label="Updated">
      {{ instance?.latest_updated }}
    </ElFormItem>
    <ElFormItem label="Results">
      <ElRow :gutter="24" style="width: 100%">
        <ElCol :span="10">
          <ElTable :data="instance?.results" border height="500">
            <ElTableColumn prop="code" label="Code" width="100" />
            <ElTableColumn prop="name" label="Name" width="100" />
            <ElTableColumn prop="date" label="Date"/>
          </ElTable>
        </ElCol>
        <ElCol :span="14">
          {{ instance?.results }}
        </ElCol>
      </ElRow>
    </ElFormItem>
  </ElForm>
</template>
