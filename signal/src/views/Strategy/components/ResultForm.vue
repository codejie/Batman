<script setup lang="ts">
import { ResultModel } from '@/api/strategy/types'
import { PropType } from 'vue'
import { ElTable, ElTableColumn } from 'element-plus'

const props = defineProps({
  results: {
    type: Array as PropType<ResultModel[]>
  }
})
</script>
<template>
  <ElTable :data="props.results" border style="width: 100%">
    <ElTableColumn prop="name" label="Name" width="120" />
    <ElTableColumn prop="type" label="Type" width="100" />
    <ElTableColumn prop="desc" label="Description" width="300" />
  </ElTable>
</template>
