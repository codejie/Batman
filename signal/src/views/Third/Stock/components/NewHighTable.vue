<script setup lang="ts">
import { apiNewHigh } from '@/api/third/stock';
import { onMounted, ref } from 'vue';
import { ElTableV2, ElAutoResizer, ElDialog, ElButton, ElText, RowEventHandlerParams } from 'element-plus';
import { KLinePanel2, ReqParam } from '@/components/KLine'

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

// type Column = {
//   name: string
//   width?: number
// }
const columnWidths = [60, 90, 90, 80, 80, 80, 90, 120]

const loading = ref<boolean>(false)
const data = ref<any[]>([]) // ref<DataFrameSetModel>()
const columns = ref<any[]>([])

const klineDialogVisible = ref<boolean>(false)
// const klineParam = ref<any>({
//   type: 1,
//   code: '',
//   name: ''
// })
const reqParam = ref<ReqParam>()
const dialogTitle = ref<string>()

async function fetchNewHigh() {
  loading.value = true

  const ret = await apiNewHigh({
    category: props.category
  })

  loading.value = false
  //columns.value = ret.result.columns.slice(1)
  const cols = ret.result.columns
  for (let i = 0; i < cols.length; ++ i) {
    columns.value.push({
      // name: cols[i],
      // width: columnWidths[i] || undefined
      key: cols[i],
      dataKey: cols[i],
      title: cols[i],
      // name: cols[i],
      width: columnWidths[i] || undefined
    })
  }
  const items = ret.result.data
  const temp:any[] = []
  items.forEach(item => {
    const d = {}
    for (let i = 0; i < columns.value.length; ++ i) {
      d[columns.value[i].dataKey] = item[i]
    }
    temp.push(d)
  })
  data.value = temp
}

function onRowClick(event: any) {
  console.log(event)
  const row = event.rowData
  console.log(row)
  dialogTitle.value = `${row['股票代码']}(${row['股票简称']})`
  // klineParam.value = {
  //   code: row['股票代码'],
  //   name: row['股票简称'],
  //   type: 1
  // }
  reqParam.value = {
    code: row['股票代码'],
    name: row['股票简称'],
    type: 1
  }
  console.log(reqParam.value)
  klineDialogVisible.value = true
}

onMounted(async () => {
  await fetchNewHigh()
})

</script>
<template>
  <ElText tag="b" class="title">{{ name }}</ElText>
  <!-- <ElTable class="table" v-loading="loading" :data="data" :border="true" highlight-current-row @row-click="onRowClick">
    <ElTableColumn type="index" width="60" />
    <ElTableColumn v-for="item in columns" :key="item.name" :label="item.name" :prop="item.name" :width="item.width" />
  </ElTable> -->
  <ElAutoResizer>
    <template #default="{width}">
      <ElTableV2 :columns="columns" :data="data" :fixed="true" :width="width" :height="600" :row-event-handlers="{ onClick: onRowClick }" />
    </template>
  </ElAutoResizer>  
  <ElDialog v-model="klineDialogVisible" :title="dialogTitle" width="60%">
    <KLinePanel2 :req-param="reqParam!" />
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
