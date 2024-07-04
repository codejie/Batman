<script setup lang="ts">
import { ref, unref } from 'vue'
import { ElRow, ElCol, ElSelect, ElOption, ElInput, ElTimePicker } from 'element-plus'

interface Props {
  mode: string
  days: string
  hour: number
  minute: number
  seconds: number
  period: boolean
}

const data = ref<Props>({
  mode: 'daily',
  days: '0-4',
  hour: 0,
  minute: 0,
  seconds: 30,
  period: false
})

defineExpose({
  data
})

const modeOptions = [
  {
    value: 'daily',
    label: '每日'
  },
  {
    value: 'delay',
    label: '延迟'
  },
  {
    value: 'interval',
    label: '周期',
    disabled: true
  }
]
const daysOptions = [
  {
    value: '0-4',
    label: '交易日'
  },
  {
    value: '0-6',
    label: '全周'
  }
]
const dailyTime = ref<Date>(new Date())
const onTimerChanged = (value) => {
  data.value.hour = unref(value)?.getHours() || 0
  data.value.minute = unref(value)?.getMinutes() || 0
}
</script>
<template>
  <!-- <ElTable :data="data" border style="width: 100%">
    <ElTableColumn label=""
  </ElTable> -->
  <ElRow :gutter="24" style="width: 100%">
    <ElCol :span="12">
      <ElRow :gutter="12" style="width: 100%">
        <ElCol :span="4" style="text-align: right">Mode</ElCol>
        <ElCol :span="20">
          <ElSelect v-model="data.mode">
            <ElOption
              v-for="item in modeOptions"
              :key="item.value"
              :value="item.value"
              :label="item.label"
              :disabled="item.disabled"
            />
          </ElSelect>
        </ElCol>
      </ElRow>
    </ElCol>
    <ElCol :span="12" v-if="data.mode == 'daily'">
      <ElRow :gutter="12" style="width: 100%">
        <ElCol :span="4" style="text-align: right">Days</ElCol>
        <ElCol :span="20">
          <ElSelect v-model="data.days">
            <ElOption
              v-for="item in daysOptions"
              :key="item.value"
              :value="item.value"
              :label="item.label"
            />
          </ElSelect>
        </ElCol>
      </ElRow>
    </ElCol>
  </ElRow>
  <ElRow :gutter="24" style="width: 100%">
    <ElCol :span="12" v-if="data.mode == 'daily'">
      <ElRow :gutter="12" style="width: 100%">
        <ElCol :span="4" style="text-align: right">Hour</ElCol>
        <ElCol :span="20">
          <ElTimePicker
            v-model="dailyTime"
            placeholder="select time"
            format="HH:mm"
            @change="onTimerChanged"
          />
        </ElCol>
      </ElRow>
    </ElCol>
    <ElCol :span="12" v-if="data.mode == 'delay'">
      <ElRow :gutter="12" style="width: 100%">
        <ElCol :span="4" style="text-align: right">Seconds</ElCol>
        <ElCol :span="20">
          <ElInput v-model="data.seconds" />
        </ElCol>
      </ElRow>
    </ElCol>
  </ElRow>
  {{ dailyTime }}
</template>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
