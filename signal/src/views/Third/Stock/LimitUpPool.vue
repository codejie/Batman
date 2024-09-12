<script setup lang="ts">
import { apiLimitUpPool } from '@/api/third/stock';
import { ContentWrap } from '@/components/ContentWrap'
import { ReqParam, KLinePanel2 } from '@/components/KLine';
import { formatToDate } from '@/utils/dateUtil';
import { ElTable, ElDialog, ElTableColumn, ElButton, ElDatePicker, ElText } from 'element-plus';
import { onMounted, ref } from 'vue';

type Column = {
  name: string
  width?: number
}
const columnWidths = [90, 90, 90, 90, 90, 90, 90, 90, 90, 120, 120, 90, 90, 80]
// const daysOptions = [7, 6, 5, 4, 3, 2, 1]

const loading = ref<boolean>(false)
const dateValue = ref<string>(getToday())
const columns = ref<Column[]>([])
const data = ref<any[]>([])
const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<ReqParam>()
const dialogTitle = ref<string>()

function getToday() {
  return formatToDate(new Date(), 'YYYYMMDD')
}

function fetch(): Promise<void> {
  loading.value = true

  data.value = []
  columns.value = []

  return new Promise<void>((resolve) =>{
    apiLimitUpPool({
      date: dateValue.value
    }).then((ret) => {
      if (ret == undefined) {
        loading.value = false
        return resolve()
      }

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
          switch (i) {
            case 2:
              item[i+1] = parseFloat(item[i+1]).toFixed(2) + '%'
              break
            case 3:
              item[i+1] = parseFloat(item[i+1]).toFixed(2)
              break
            case 4:
              // item[i+1] = (parseFloat(item[i+1]) / 10000).toFixed(2) + '万'
              // break
            case 5:
            case 6:
            case 8:
              item[i+1] = (parseFloat(item[i+1]) / 100000000).toFixed(2) + '亿'
              break
            case 7:
              item[i+1] = (parseFloat(item[i+1])).toFixed(2) + '%'
              break
            case 9:
            case 10:
              item[i+1] = item[i+1].replace(/(.{2})/g, `$1:`).slice(0, -1)
              // item[i+1] = item[i+1].replace(new RegExp(`(.{2})`, 'g'), '$1' + ':').slice(0, -1)
              break
          }
          d[columns.value[i].name] = item[i+1]
        }
        data.value.push(d)
      })
      loading.value = false
      resolve()
    })
  })
}

onMounted(async () => {
  await fetch()
})

function onRowClick(row: any) {
  dialogTitle.value = `${row['代码']}(${row['名称']})`
  reqParam.value = {
    code: row['代码'],
    name: row['名称'],
    type: 1
  }
  klineDialogVisible.value = true
}

function isworkday(date) {
  const today = new Date()

  if (date.date > today || date.date < today.setDate(today.getDate() - 20))
    return 'text'
  return date.date.getDay() == 0 || date.date.getDay() == 6 ? 'text': 'workday'
}

async function onDateChanged(value) {
  if (value > getToday())
    dateValue.value = getToday()
  await fetch()
}

</script>
<template>
  <ContentWrap title="涨停股池">
    <div class="title">
      <ElText tag="b" style="padding-right: 8px;">日期</ElText>
      <ElDatePicker v-model="dateValue" type="date" format="YYYY-MM-DD" value-format="YYYYMMDD" @change="onDateChanged" >
        <template #default="cell">
          <div class="cell" :class="{ current: cell.isCurrent }">
            <span :class="isworkday(cell)">{{ cell.text }}</span>
        </div>
        </template>
      </ElDatePicker>
    </div>
    <ElTable class="table" v-loading="loading" :data="data" :border="true" highlight-current-row @row-click="onRowClick">
      <ElTableColumn type="index" width="60" />
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

.cell {
  height: 30px;
  padding: 3px 0;
  box-sizing: border-box;
}

.cell .text {
  width: 24px;
  height: 24px;
  display: block;
  margin: 0 auto;
  line-height: 24px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 50%;
}

.cell.current .text {
  background: #626aef;
  color: #fff;
}

.cell .workday {
  width: 24px;
  height: 24px;
  display: block;
  margin: 0 auto;
  line-height: 24px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 50%;  
  color: black;
  font-weight: bold;
}

.cell.current .workday {
  background: #626aef;
  color: #fff;
}
</style>

