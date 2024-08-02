<script setup lang="ts">
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { apiInfos } from '@/api/customized';
import { InfoModel } from '@/api/customized/types';
import { apiHistory } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { onMounted, ref } from 'vue';
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn } from 'element-plus'
import { useRouter } from 'vue-router';
import { ShowParam, KLinePanel3 } from '@/components/KLine';

const { go } = useRouter()

const DEFAULT_START = '2024-01-01'
const DEFAULT_END = undefined

const props = defineProps({
  code: {
    type: String,
    required: true
  }
})

const colSpan = ref<any>({
  left: 3,
  middle: 17,
  right: 4
})
const selectCode = ref<string>(props.code)
const customizedList = ref<InfoModel[]>()
const historyData = ref<HistoryDataModel[]>([])
const showParam = ref<ShowParam>({
  maLines: [5, 12, 30 ],
  hideVolume: false,
  markLines: true
})

async function fetchCustomized() {
  const ret = await apiInfos({})
  customizedList.value = ret.result
}

async function fetchHistory(code: string) {
  const ret = await apiHistory({
    code: code,
    start: DEFAULT_START,
    end: DEFAULT_END
  })
  historyData.value = ret.result
}

onMounted(async () => {
    await fetchCustomized()
    await fetchHistory(props.code)
  }
)

function makeTitle() {
  return `${props.code}`
}

function onTestClick() {
  if (colSpan.value.left == 0) {
    colSpan.value = {
      left: 3,
      middle: 17,
      right: 4      
    }
  } else {
    colSpan.value = {
      left: 0,
      middle: 20,
      right: 4
    }
  }

  showParam.value = {
    maLines: [5, 12, 30 ],
    hideVolume: false,
    markLines: true
  }
}

async function onCustomizedClick(row: any) {
  selectCode.value = row.code
  await fetchHistory(selectCode.value)
}
</script>
<template>
  <ContentDetailWrap :title="makeTitle()">
    <template #header>
      <ElButton @click="go(-1)">Back</ElButton>
      <ElButton @click="onTestClick">Test</ElButton>
    </template>
    <ElRow :gutter="24">
      <ElCol class="middle-col" :span="colSpan.left">
        <ElTable :data="customizedList" @row-click="onCustomizedClick" :border="true" max-height="800" width="auto" highlight-current-row>
          <ElTableColumn prop="code" label="Code" width="90" />
          <ElTableColumn prop="name" label="Name" />
        </ElTable>
      </ElCol>
      <ElCol class="middle-col" :span="colSpan.middle">
        <ElRow :gutter="24">
          <div>Tools</div>
        </ElRow>
        <ElRow :gutter="24">
          <div style="width: 100%; height: 100%;">
            <KLinePanel3 :data="historyData" :showParam="showParam" />
          </div>
        </ElRow>
        <ElRow class="middle-col" :gutter="24">
          <ElTable :data="historyData" :stripe="true" :border="true" max-height="300" style="width: 100%;">
            <ElTableColumn prop="date" label="日期" width="120" />            
            <ElTableColumn prop="price" label="现价" width="100" />
            <ElTableColumn prop="percentage" label="涨跌幅%" width="100" />
            <ElTableColumn prop="amount" label="涨跌额" width="100" />
            <ElTableColumn prop="volatility" label="振幅%" width="100" />          
            <ElTableColumn prop="open" label="今开" width="100" />
            <ElTableColumn prop="close" label="昨收" width="100" />
            <ElTableColumn prop="high" label="最高" width="100" />
            <ElTableColumn prop="low" label="最低" width="100" />
            <ElTableColumn prop="volume" label="成交量" width="120" />
            <ElTableColumn prop="turnover" label="成交额" width="140" />
            <ElTableColumn prop="rate" label="换手率%" width="100" />
          </ElTable>          
        </ElRow>
      </ElCol>
      <ElCol class="middle-col" :span="colSpan.right">
        {{ selectCode }}
      </ElCol>      
    </ElRow>
  </ContentDetailWrap>
</template>
<style lang="css">
.middle-col {
  padding: 8px;
  outline: 1px solid gainsboro;
  outline-offset:-4px;   
}
</style>
