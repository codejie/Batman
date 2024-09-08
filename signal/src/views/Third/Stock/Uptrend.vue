<script setup lang="ts">
import { apiUptrend } from '@/api/third/stock';
import { ContentWrap } from '@/components/ContentWrap'
import { ReqParam, KLinePanel2 } from '@/components/KLine';
import { ElText, ElSelect, ElOption, ElTable, ElDialog, ElTableColumn, ElButton } from 'element-plus';
import { onMounted, ref } from 'vue';

type Column = {
  name: string
  width?: number
}
const columnWidths = [90, 90, 80, 80, 80, 90, 100, 100]
const daysOptions = [9, 8, 7, 6, 5, 4, 3, 2, 1]

const days = ref<number>(3)
const columns = ref<Column[]>([])
const data = ref<any[]>([])
const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<ReqParam>()
const dialogTitle = ref<string>()

function fetch(): Promise<void> {
  data.value = []
  columns.value = []

  return new Promise<void>((resolve) =>{
    apiUptrend({
      days: days.value
    }).then((ret) => {
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
      resolve()
    })
  })
}

onMounted(async () => {
  await fetch()
})

function onRowClick(row: any) {
  dialogTitle.value = `${row['股票代码']}(${row['股票简称']})`
  reqParam.value = {
    code: row['股票代码'],
    name: row['股票简称'],
    type: 1
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
    <ElTable class="table" :data="data" :border="true" highlight-current-row @row-click="onRowClick">
      <ElTableColumn v-for="item in columns" :key="item.name" :label="item.name" :prop="item.name" :width="item.width" />
    </ElTable>
    <ElDialog v-model="klineDialogVisible" :title="dialogTitle" width="60%" :destroy-on-close="true">
      <KLinePanel2 :req-param="reqParam" />
      <template #footer>
        <ElButton type="primary" @click="klineDialogVisible=false">Close</ElButton>
      </template>    
    </ElDialog>    
  </ContentWrap>
</template>
<style lang="css">
.title {
  padding: 14px;
}
</style>

