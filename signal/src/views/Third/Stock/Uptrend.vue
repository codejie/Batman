<script setup lang="ts">
import { TYPE_STOCK } from '@/api/data';
import { apiUptrend } from '@/api/third';
import { ContentWrap } from '@/components/ContentWrap'
import { ReqParam } from '@/components/KLine';
import { ElText, ElSelect, ElOption, ElTableV2, ElAutoResizer } from 'element-plus';
import { onMounted, ref } from 'vue';
import KDialog from './components/KDialog.vue';

// type Column = {
//   name: string
//   width?: number
// }
const columnWidths = [60, 90, 90, 80, 80, 80, 90, 100, 100, 120]
const daysOptions = [9, 8, 7, 6, 5, 4, 3, 2, 1]

const loading = ref<boolean>(false)
const days = ref<number>(3)
const columns = ref<any[]>([])
const data = ref<any[]>([])
const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<ReqParam>()
const dialogTitle = ref<string>()

function fetch(): Promise<void> {
  data.value = []
  columns.value = []

  return new Promise<void>((resolve) =>{
    loading.value = true

    apiUptrend({
      days: days.value
    }).then((ret) => {
      const cols = ret.result.columns
      for (let i = 0; i < cols.length; ++ i) {
        columns.value.push({
          key: cols[i],
          dataKey: cols[i],
          title: cols[i],
          width: columnWidths[i] || undefined
        })
      }

      const items = ret.result.data
      const temp: any[] = []
      items.forEach(item => {
        const d = {}
        for (let i = 0; i < columns.value.length; ++ i) {
          d[columns.value[i].dataKey] = item[i]
        }
        temp.push(d)
      })

      data.value = temp
      loading.value = false
      resolve()
    })
  })
}

onMounted(async () => {
  await fetch()
})

function onRowClick(event: any) {
  const row = event.rowData
  dialogTitle.value = `${row['股票简称']} (${row['股票代码']})`
  reqParam.value = {
    code: row['股票代码'],
    name: row['股票简称'],
    type: TYPE_STOCK
  }
  klineDialogVisible.value = true
}

async function onDaysChanged() {
  await fetch()
}

</script>
<template>
  <ContentWrap title="连续上涨">
    <div class="title">
      <ElText tag="b" style="padding-right: 4px;">连续上涨天数大于</ElText>
      <ElSelect v-model="days" style="width: 60px;" @change="onDaysChanged">
        <ElOption v-for="i in daysOptions" :key="i" :value="i" :label="i" />
      </ElSelect>
      <ElText tag="b" style="padding-left: 4px;">天</ElText>
    </div>
    <!-- <ElTable class="table" v-loading="loading" :data="data" :border="true" highlight-current-row @row-click="onRowClick">
      <ElTableColumn type="index" width="60" />
      <ElTableColumn v-for="item in columns" :key="item.name" :label="item.name" :prop="item.name" :width="item.width" />
    </ElTable> -->
    <ElAutoResizer>
      <template #default="{width}">
        <ElTableV2 :columns="columns" :data="data" :fixed="true" :width="width" :row-event-handlers="{ onClick: onRowClick }" :height="700"/>
      </template>
    </ElAutoResizer>  
    <!-- <ElDialog v-model="klineDialogVisible" :title="dialogTitle" width="60%" :destroy-on-close="true">
      <KLinePanel2 :req-param="reqParam!" />
      <template #footer>
        <ElButton type="primary" @click="klineDialogVisible=false">关闭</ElButton>
      </template>    
    </ElDialog>     -->
    <KDialog :visible ="klineDialogVisible" :req-param="reqParam" @update:on-close="klineDialogVisible = false" />
  </ContentWrap>
</template>
<style lang="css">
.title {
  padding: 14px;
}
</style>

