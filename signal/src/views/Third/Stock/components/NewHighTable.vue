<script setup lang="ts">
import { apiNewHigh } from '@/api/third/stock';
import { DataFrameSetModel } from '@/api/third/stock/types';
import { onMounted, ref } from 'vue';
import { ElTable, ElTableColumn } from 'element-plus';

const props = defineProps({
  category: {
    type: Number,
    required: true
  },
  name: {
    type: String,
    required: true
  }
})

type Column = {
  name: string
  width?: number
}
const columnWidths = [90, 90, 80, 80, 80, 90, 120]

const data = ref<any[]>([]) // ref<DataFrameSetModel>()
const columns = ref<Column[]>([])

async function fetchNewHigh() {
  const ret = await apiNewHigh({
    category: props.category
  })
  //columns.value = ret.result.columns.slice(1)
  const cols = ret.result.columns
  for (let i = 1; i < cols.length; ++ i) {
    columns.value.push({
      name: cols[i],
      width: columnWidths[i - 1] || undefined
    })
  }
  const items = ret.result.data
  items.forEach(item => {
    const d = {}
    for (let i = 0; i < columns.value.length; ++ i) {
      d[columns.value[i].name] = item[i+1]
    }
    data.value.push(d)
  })
}

function onRowClick(row: any) {

}

onMounted(async () => {
  await fetchNewHigh()
})
</script>
<template>
  <div class="title">{{ name }}</div>
  <ElTable class="table" :data="data" :border="true" highlight-current-row @row-click="onRowClick">
    <ElTableColumn v-for="item in columns" :key="item.name" :label="item.name" :prop="item.name" :width="item.width" />
  </ElTable>
</template>
<style lang="css">
.title {
  margin: 4px;
}
.table {
  padding: 8px;
  outline: 1px solid gainsboro;
  /* outline-offset:-4px;    */
}
</style>
