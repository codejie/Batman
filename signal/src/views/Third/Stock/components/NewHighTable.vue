<script setup lang="ts">
import { apiNewHigh } from '@/api/third/stock';
import { onMounted, ref } from 'vue';
import { ElTable, ElTableColumn, ElDialog, ElButton } from 'element-plus';
import { KLinePanel } from '@/components/KLine'

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

const klineDialogVisible = ref<boolean>(false)
const klineParam = ref<any>({
  type: 1,
  code: '',
  name: ''
})
const dialogTitle = ref<string>()

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
  dialogTitle.value = `${row['股票代码']}(${row['股票简称']})`
  klineParam.value = {
    code: row['股票代码'],
    name: row['股票简称'],
    type: 1
  }
  klineDialogVisible.value = true
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
  <ElDialog v-model="klineDialogVisible" :title="dialogTitle" width="60%">
    <KLinePanel :param="klineParam" />
    <template #footer>
        <ElButton type="primary" @click="klineDialogVisible=false">Close</ElButton>
      </template>    
  </ElDialog>
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
