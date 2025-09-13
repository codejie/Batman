<script setup lang="ts">
import { TYPE_STOCK } from '@/api/data'
import { apiLimitUpPool } from '@/api/third'
import { ContentWrap } from '@/components/ContentWrap'
import { ReqParam } from '@/components/KLine'
import { formatToDate } from '@/utils/dateUtil'
import { ElDatePicker, ElText, ElTableV2, ElAutoResizer } from 'element-plus'
import { onMounted, ref } from 'vue'
import KDialog from './components/KDialog.vue'

// type Column = {
//   name: string
//   width?: number
// }
const columnWidths = [60, 90, 90, 90, 90, 90, 90, 90, 90, 90, 120, 120, 90, 90, 80, 120, 100]
// const daysOptions = [7, 6, 5, 4, 3, 2, 1]

const loading = ref<boolean>(false)
const dateValue = ref<string>()
const columns = ref<any[]>([])
const data = ref<any[]>([])
const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<ReqParam>()
const dialogTitle = ref<string>()

function getToday() {
  return formatToDate(new Date(), 'YYYYMMDD')
}

function fetch(): Promise<void> {
  loading.value = true

  // data.value = []
  // columns.value = []
  const temp_data: any[] = []
  const temp_columns: any[] = []
  return new Promise<void>((resolve) => {
    apiLimitUpPool({
      date: dateValue.value
    }).then((ret) => {
      if (ret == undefined) {
        loading.value = false
        return resolve()
      }

      const cols = ret.result.columns
      for (let i = 0; i < cols.length; ++i) {
        temp_columns.push({
          key: cols[i],
          dataKey: cols[i],
          title: cols[i],
          // name: cols[i],
          width: columnWidths[i] || undefined
        })
      }

      //   temp_columns.push({
      //     key: 'Action',
      //     dateKey: 'Action',
      //     title: '操作',
      //     width: 90,
      //     cellRenderer: () => (
      //   <>
      //     <ElButton size="small">Edit</ElButton>
      //   </>
      // )
      //   })

      const items = ret.result.data
      items.forEach((item) => {
        const d = {}
        for (let i = 0; i < temp_columns.length; ++i) {
          switch (i) {
            case 3:
              item[i] = parseFloat(item[i]).toFixed(2) + '%'
              break
            case 4:
              item[i] = parseFloat(item[i]).toFixed(2)
              break
            case 5:
            // item[i] = (parseFloat(item[i]) / 10000).toFixed(2) + '万'
            // break
            case 6:
            case 7:
            case 9:
              item[i] = (parseFloat(item[i]) / 100000000).toFixed(2) + '亿'
              break
            case 8:
              item[i] = parseFloat(item[i]).toFixed(2) + '%'
              break
            case 10:
            case 11:
              item[i] = item[i].replace(/(.{2})/g, `$1:`).slice(0, -1)
              // item[i] = item[i].replace(new RegExp(`(.{2})`, 'g'), '$1' + ':').slice(0, -1)
              break
          }
          d[temp_columns[i].dataKey] = item[i]
        }
        temp_data.push(d)
      })
      data.value = temp_data
      columns.value = temp_columns
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
  dialogTitle.value = `${row['代码']}(${row['名称']})`
  reqParam.value = {
    code: row['代码'],
    name: row['名称'],
    type: TYPE_STOCK
  }
  klineDialogVisible.value = true
}

function isworkday(date) {
  const today = new Date()

  if (date.date > today || date.date < today.setDate(today.getDate() - 20)) return 'text'
  return date.date.getDay() == 0 || date.date.getDay() == 6 ? 'text' : 'workday'
}

async function onDateChanged(value) {
  if (value > getToday()) dateValue.value = getToday()
  await fetch()
}
</script>
<template>
  <ContentWrap title="涨停股池">
    <div class="title">
      <ElText tag="b" style="padding-right: 8px">日期</ElText>
      <ElDatePicker
        v-model="dateValue"
        type="date"
        format="YYYY-MM-DD"
        value-format="YYYYMMDD"
        @change="onDateChanged"
      >
        <template #default="cell">
          <div class="cell" :class="{ current: cell.isCurrent }">
            <span :class="isworkday(cell)">{{ cell.text }}</span>
          </div>
        </template>
      </ElDatePicker>
    </div>
    <ElAutoResizer>
      <template #default="{ width }">
        <ElTableV2
          :columns="columns"
          :data="data"
          :fixed="true"
          :width="width"
          :row-event-handlers="{ onClick: onRowClick }"
          :height="700"
        />
      </template>
    </ElAutoResizer>
    <!-- <ElTableV2 :columns="columns" :data="data" :fixed="true" :width="1600" :height="600"/> -->
    <!-- <ElTable class="table" v-loading="loading" :data="data" :border="true" highlight-current-row @row-click="onRowClick">
      <ElTableColumn type="index" width="60" />
      <ElTableColumn v-for="item in columns" :key="item.name" :label="item.name" :prop="item.name" :width="item.width" />
    </ElTable> -->
    <!-- <ElDialog v-model="klineDialogVisible" :title="dialogTitle" width="60%" :destroy-on-close="true">
      <KLinePanel2 :req-param="reqParam!" />
      <template #footer>
        <ElButton type="primary" @click="klineDialogVisible=false">关闭</ElButton>
      </template>    
    </ElDialog>     -->
    <KDialog
      :visible="klineDialogVisible"
      :req-param="reqParam"
      @update:on-close="klineDialogVisible = false"
    />
  </ContentWrap>
</template>
<style lang="css">
.title {
  padding: 14px;
}

.cell {
  height: 30px;
  padding: 3px 0;
  box-sizing: border-box;
}

.cell .text {
  position: absolute;
  left: 50%;
  display: block;
  width: 24px;
  height: 24px;
  margin: 0 auto;
  line-height: 24px;
  border-radius: 50%;
  transform: translateX(-50%);
}

.cell.current .text {
  color: #fff;
  background: #626aef;
}

.cell .workday {
  position: absolute;
  left: 50%;
  display: block;
  width: 24px;
  height: 24px;
  margin: 0 auto;
  font-weight: bold;
  line-height: 24px;
  color: black;
  border-radius: 50%;
  transform: translateX(-50%);
}

.cell.current .workday {
  color: #fff;
  background: #626aef;
}
</style>
