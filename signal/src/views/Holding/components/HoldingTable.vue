<script setup lang="ts">
import { ElButton, ElTable, ElTableColumn, ElDialog } from 'element-plus';
import { PropType, ref } from 'vue';
import { KLinePanel2, ReqParam } from '@/components/KLine'

export type ColumnOpt = {
  name: string,
  label: string,
  width: number,
}

export type ActionOpt = {
  name: string,
  type?: string,
  func: Function
}

defineProps({
  data: {
    type: Array as PropType<Object[]>,
    default: () => [],
    required: false
  },
  columns: {
    type: Array as PropType<ColumnOpt[]>,
    required: true
  },
  actions: {
    type: Array as PropType<ActionOpt[]>,
    required: false,
    default: () => []
  }
})

const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<ReqParam>()
const dialogTitle = ref<string>()

function onRowClick(row: any) {
  dialogTitle.value = `${row.code}(${row.name})`
  reqParam.value = {
    code: row.code,
    name: row.name,
    type: row.type
  }
  klineDialogVisible.value = true
}

function getBtnType(type?: string): any {
  return type || 'default'
}
</script>

<template>
  <ElTable :data="data" :border="true" :highlight-current-row="true" @row-click="onRowClick">
    <ElTableColumn type="index" width="50" />
    <ElTableColumn v-for="item in columns" :key="item.name" :label="item.label" :prop="item.name" :width="item.width" />
    <ElTableColumn label="Action">
      <template #default="{row}">
        <ElButton link v-for="btn in actions" :type="getBtnType(btn.type)" :key="btn.name" @click.stop="btn.func(row)">{{ btn.name }}</ElButton>
      </template>
    </ElTableColumn>
  </ElTable>
  <ElDialog v-model="klineDialogVisible" :title="dialogTitle" width="60%" :destroy-on-close="true">
    <KLinePanel2 :req-param="reqParam!" />
    <template #footer>
      <ElButton type="primary" @click="klineDialogVisible=false">Close</ElButton>
    </template>    
  </ElDialog>  
</template>
