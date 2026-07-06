<script setup lang="ts">
import { apiDownloadList, TYPE_STOCK, TYPE_INDEX } from '@/api/data'
import {
  apiDbExport,
  apiDbRemoveAllHistoryData,
  apiGetDataConfig,
  apiGetTradeCalendar,
  apiSaveDataConfig,
  apiSaveTradeCalendar,
  urlDbImport
} from '@/api/system'
import type { MarketDataSource } from '@/api/system/types'
import { ContentWrap } from '@/components/ContentWrap'
import {
  ElButton,
  ElDialog,
  ElInputNumber,
  ElOption,
  ElSelect,
  ElUpload,
  UploadInstance,
  ElMessage,
  ElMessageBox
} from 'element-plus'
import { Calendar, Check, Delete, Download, Refresh, Setting, Upload } from '@element-plus/icons-vue'
import { computed, ref } from 'vue'

interface CalendarDay {
  date: string
  day: number
  month: number
  weekday: number
  isWeekend: boolean
  isTradeDay: boolean
}

const uploadRef = ref<UploadInstance>()
const showSubmit = ref(false)
const dataSourceVisible = ref(false)
const dataSourceLoading = ref(false)
const dataSourceSaving = ref(false)
const marketDataSource = ref<MarketDataSource>('akshare')
const tradeCalendarVisible = ref(false)
const tradeCalendarLoading = ref(false)
const tradeCalendarSaving = ref(false)
const tradeCalendarYear = ref(new Date().getFullYear())
const tradeDaySet = ref<Set<string>>(new Set())
const calendarSource = ref<'default' | 'saved'>('default')

const monthLabels = [
  '一月',
  '二月',
  '三月',
  '四月',
  '五月',
  '六月',
  '七月',
  '八月',
  '九月',
  '十月',
  '十一月',
  '十二月'
]
const weekdayLabels = ['一', '二', '三', '四', '五', '六', '日']
const marketDataSourceOptions: { label: string; value: MarketDataSource }[] = [
  { label: '东方财富', value: 'akshare' },
  { label: '腾讯财经', value: 'tencent' }
]

async function onExport() {
  await apiDbExport({})
}

async function onImport() {
  const retConfirm = await ElMessageBox.confirm('是否提交数据?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
  if (retConfirm === 'confirm') {
    uploadRef.value?.submit()
    uploadRef.value?.clearFiles()

    showSubmit.value = false
  }
}
function onUploadChange() {
  showSubmit.value = true
}

function onUploadRemove() {
  showSubmit.value = false
}

async function onDownloadList(type: number) {
  const retConfirm = await ElMessageBox.confirm('是否更新列表信息?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
  if (retConfirm === 'confirm') {
    const ret = await apiDownloadList({
      type: type
    })
    if (ret.code == 0) {
      ElMessage.success('更新成功.')
    } else {
      ElMessage.error('更新失败.')
    }
  }
}

async function onHistoryDelete() {
  const retConfirm = await ElMessageBox.confirm('是否清除所有历史数据?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
  if (retConfirm === 'confirm') {
    const ret = await apiDbRemoveAllHistoryData({})
    if (ret.code == 0) {
      ElMessage.success('清除成功.')
    } else {
      ElMessage.error('清除失败.')
    }
  }
}

async function loadDataConfig() {
  dataSourceLoading.value = true
  try {
    const ret = await apiGetDataConfig({})
    marketDataSource.value = ret.result.market_data_source
  } finally {
    dataSourceLoading.value = false
  }
}

async function onDataSourceOpen() {
  dataSourceVisible.value = true
  await loadDataConfig()
}

async function onDataSourceSave() {
  dataSourceSaving.value = true
  try {
    const ret = await apiSaveDataConfig({
      market_data_source: marketDataSource.value
    })
    marketDataSource.value = ret.result.market_data_source
    dataSourceVisible.value = false
    ElMessage.success('数据源配置已保存.')
  } finally {
    dataSourceSaving.value = false
  }
}

function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = `${date.getMonth() + 1}`.padStart(2, '0')
  const day = `${date.getDate()}`.padStart(2, '0')
  return `${year}-${month}-${day}`
}

function getYearDates(year: number): string[] {
  const ret: string[] = []
  const current = new Date(year, 0, 1)
  while (current.getFullYear() === year) {
    ret.push(formatDate(current))
    current.setDate(current.getDate() + 1)
  }
  return ret
}

const yearDates = computed(() => getYearDates(tradeCalendarYear.value))

const nonTradeDays = computed(() => {
  return yearDates.value.filter((date) => !tradeDaySet.value.has(date))
})

const tradeCalendarMonths = computed(() => {
  const months: CalendarDay[][] = Array.from({ length: 12 }, () => [])
  for (const date of yearDates.value) {
    const current = new Date(`${date}T00:00:00`)
    const weekday = current.getDay()
    const normalizedWeekday = weekday === 0 ? 7 : weekday
    months[current.getMonth()].push({
      date,
      day: current.getDate(),
      month: current.getMonth(),
      weekday: normalizedWeekday,
      isWeekend: normalizedWeekday >= 6,
      isTradeDay: tradeDaySet.value.has(date)
    })
  }
  return months
})

async function loadTradeCalendar() {
  tradeCalendarLoading.value = true
  try {
    const ret = await apiGetTradeCalendar({
      year: tradeCalendarYear.value
    })
    tradeDaySet.value = new Set(ret.result.trade_days)
    calendarSource.value = ret.result.source
  } finally {
    tradeCalendarLoading.value = false
  }
}

async function onTradeCalendarOpen() {
  tradeCalendarVisible.value = true
  await loadTradeCalendar()
}

async function onTradeCalendarYearChanged() {
  await loadTradeCalendar()
}

function onTradeDayToggle(date: string) {
  const next = new Set(tradeDaySet.value)
  if (next.has(date)) {
    next.delete(date)
  } else {
    next.add(date)
  }
  tradeDaySet.value = next
}

async function onTradeCalendarSave() {
  tradeCalendarSaving.value = true
  try {
    const ret = await apiSaveTradeCalendar({
      year: tradeCalendarYear.value,
      trade_days: Array.from(tradeDaySet.value).sort(),
      non_trade_days: nonTradeDays.value
    })
    tradeDaySet.value = new Set(ret.result.trade_days)
    calendarSource.value = ret.result.source
    ElMessage.success('交易日配置已保存.')
  } finally {
    tradeCalendarSaving.value = false
  }
}
</script>

<template>
  <ContentWrap title="系统配置">
    <div class="configuration-actions">
      <section class="config-section">
        <div class="section-header">
          <div class="section-title">导出导入</div>
        </div>
        <div class="action-row">
          <ElButton type="primary" plain :icon="Download" @click="onExport">持仓数据导出</ElButton>
          <ElUpload
            ref="uploadRef"
            class="import-upload"
            :action="urlDbImport"
            :multiple="false"
            :auto-upload="false"
            :on-change="onUploadChange"
            :on-remove="onUploadRemove"
          >
            <template #trigger>
              <ElButton type="primary" plain :icon="Upload">持仓数据导入</ElButton>
            </template>
            <ElButton v-if="showSubmit" type="primary" plain :icon="Check" @click="onImport">
              提交
            </ElButton>
          </ElUpload>
        </div>
      </section>

      <section class="config-section">
        <div class="section-header">
          <div class="section-title">数据配置</div>
        </div>
        <div class="action-row">
          <ElButton type="primary" plain :icon="Setting" @click="onDataSourceOpen">
            数据源配置
          </ElButton>
          <ElButton type="primary" plain :icon="Calendar" @click="onTradeCalendarOpen">
            交易日配置
          </ElButton>
        </div>
      </section>

      <section class="config-section">
        <div class="section-header">
          <div class="section-title">数据更新</div>
        </div>
        <div class="action-row">
          <ElButton type="primary" plain :icon="Refresh" @click="onDownloadList(TYPE_STOCK)">
            股票列表信息
          </ElButton>
          <ElButton type="primary" plain :icon="Refresh" @click="onDownloadList(TYPE_INDEX)">
            指数列表信息
          </ElButton>
        </div>
      </section>

      <section class="config-section danger-section">
        <div class="section-header">
          <div class="section-title">数据清除</div>
        </div>
        <div class="action-row">
          <ElButton type="danger" plain :icon="Delete" @click="onHistoryDelete()">
            清除历史数据
          </ElButton>
        </div>
      </section>
    </div>

    <ElDialog v-model="dataSourceVisible" title="数据源配置" width="420px">
      <div v-loading="dataSourceLoading" class="data-source-form">
        <span class="toolbar-label">数据源</span>
        <ElSelect v-model="marketDataSource" class="data-source-select">
          <ElOption
            v-for="item in marketDataSourceOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </ElSelect>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <ElButton @click="dataSourceVisible = false">关闭</ElButton>
          <ElButton type="primary" :loading="dataSourceSaving" @click="onDataSourceSave">
            保存
          </ElButton>
        </div>
      </template>
    </ElDialog>

    <ElDialog
      v-model="tradeCalendarVisible"
      title="交易日配置"
      width="1180px"
      top="4vh"
      class="trade-calendar-dialog"
    >
      <div class="calendar-toolbar">
        <div class="year-control">
          <span class="toolbar-label">年份</span>
          <ElInputNumber
            v-model="tradeCalendarYear"
            :min="2000"
            :max="2100"
            :step="1"
            controls-position="right"
            @change="onTradeCalendarYearChanged"
          />
        </div>
        <div class="calendar-summary">
          <span>交易日 {{ tradeDaySet.size }} 天</span>
          <span>非交易日 {{ nonTradeDays.length }} 天</span>
          <span>{{ calendarSource === 'saved' ? '已保存配置' : '默认配置' }}</span>
        </div>
      </div>

      <div v-loading="tradeCalendarLoading" class="calendar-grid">
        <section v-for="(days, monthIndex) in tradeCalendarMonths" :key="monthIndex" class="month-panel">
          <div class="month-title">{{ monthLabels[monthIndex] }}</div>
          <div class="weekday-grid">
            <span v-for="label in weekdayLabels" :key="label">{{ label }}</span>
          </div>
          <div class="day-grid">
            <span
              v-for="offset in days[0]?.weekday - 1 || 0"
              :key="`offset-${monthIndex}-${offset}`"
              class="day-cell day-placeholder"
            />
            <button
              v-for="day in days"
              :key="day.date"
              class="day-cell"
              :class="{
                'is-trade-day': day.isTradeDay,
                'is-non-trade-day': !day.isTradeDay,
                'is-weekend': day.isWeekend
              }"
              :title="`${day.date} ${day.isTradeDay ? '交易日' : '非交易日'}`"
              @click="onTradeDayToggle(day.date)"
            >
              {{ day.day }}
            </button>
          </div>
        </section>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <ElButton @click="tradeCalendarVisible = false">关闭</ElButton>
          <ElButton type="primary" :loading="tradeCalendarSaving" @click="onTradeCalendarSave">
            保存
          </ElButton>
        </div>
      </template>
    </ElDialog>
  </ContentWrap>
</template>

<style scoped>
.configuration-actions {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.config-section {
  padding: 16px 18px;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
  background: var(--el-fill-color-blank);
}

.danger-section {
  border-color: var(--el-color-danger-light-7);
  background: var(--el-color-danger-light-9);
}

.section-header {
  display: flex;
  align-items: center;
  min-height: 24px;
  margin-bottom: 14px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.import-upload {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.import-upload :deep(.el-upload) {
  display: inline-flex;
  align-items: center;
}

.import-upload :deep(.el-upload-list) {
  flex-basis: 100%;
  margin: 4px 0 0;
}

.import-upload :deep(.el-upload-list:empty) {
  display: none;
}

.data-source-form {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr);
  gap: 12px;
  align-items: center;
}

.data-source-select {
  width: 100%;
}

.calendar-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.year-control,
.calendar-summary,
.dialog-footer {
  display: flex;
  gap: 12px;
  align-items: center;
}

.dialog-footer {
  justify-content: flex-end;
}

.toolbar-label {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.calendar-summary {
  flex-wrap: wrap;
  color: var(--el-text-color-regular);
}

.calendar-summary span {
  padding: 4px 10px;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 999px;
  background: var(--el-fill-color-light);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  max-height: 68vh;
  overflow: auto;
  padding-right: 4px;
}

.month-panel {
  padding: 10px;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
  background: var(--el-fill-color-blank);
}

.month-title {
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.weekday-grid,
.day-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.weekday-grid {
  margin-bottom: 5px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  text-align: center;
}

.day-cell {
  width: 100%;
  min-width: 0;
  height: 28px;
  padding: 0;
  border: 1px solid transparent;
  border-radius: 6px;
  font-size: 12px;
  line-height: 26px;
  text-align: center;
  cursor: pointer;
}

.day-placeholder {
  cursor: default;
}

.is-trade-day {
  border-color: var(--el-color-primary-light-5);
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.is-non-trade-day {
  border-color: var(--el-border-color-lighter);
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
}

.is-weekend.is-non-trade-day {
  background: var(--el-fill-color);
}

.day-cell:hover:not(.day-placeholder) {
  border-color: var(--el-color-primary);
}

@media (max-width: 1100px) {
  .calendar-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 820px) {
  .calendar-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 560px) {
  .calendar-grid {
    grid-template-columns: 1fr;
  }
}
</style>
