<script setup lang="ts">
import { ElButton, ElTable, ElTableColumn } from 'element-plus';
import { PropType } from 'vue';

export type ColumnOpt = {
  name: string,
  label: string,
  width: number,
  extend?: any
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

function getBtnType(type?: string): any {
  return type || 'default'
}
</script>

<template>
  <ElTable :data="data" :border="true" :highlight-current-row="true">
    <ElTableColumn type="index" width="60" />
    <ElTableColumn v-for="item in columns" :key="item.name" :label="item.label" :prop="item.name" :width="item.width" />
    <ElTableColumn label="Action">
      <template #default="{row}">
        <ElButton link v-for="btn in actions" :type="getBtnType(btn.type)" :key="btn.name" @click.stop="btn.func(row)">{{ btn.name }}</ElButton>
      </template>
    </ElTableColumn>
  </ElTable>
</template>
