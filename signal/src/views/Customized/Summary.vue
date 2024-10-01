<script setup lang="ts">
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { apiInfos } from '@/api/customized';
import { InfoModel } from '@/api/customized/types';
import { onMounted, ref } from 'vue';
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn } from 'element-plus'
import { useRouter } from 'vue-router';
import { KLinePanel, ReqParam } from '@/components/KLine';
import MarginTable from './components/MarginTable.vue';

const { go } = useRouter()

// const DEFAULT_START = '2024-01-01'
// const DEFAULT_END = undefined

const props = defineProps({
  type: {
    type: String,
    required: true
  },
  code: {
    type: String,
    required: true
  },
  name: {
    type: String,
    required: true
  }
})

const colSpan = ref<any>({
  left: 4,
  middle: 20,
  right: 0
})
const selectType = ref<number>(parseInt(props.type))
const selectCode = ref<string>(props.code)
const customizedList = ref<InfoModel[]>()

async function fetchCustomized() {
  const ret = await apiInfos({})
  customizedList.value = ret.result
}

onMounted(async () => {
    await fetchCustomized()
    // await fetchHistory(props.code)
  }
)

function makeTitle() {
  return `${props.code}(${props.name})`
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
}

async function onCustomizedClick(row: any) {
  selectType.value = row.type
  selectCode.value = row.code
  // await fetchHistory(selectCode.value)
  param.value = {
    type: row.type,
    code: row.code,
    name: row.name
  }
}

const param = ref<ReqParam>({
  type: parseInt(props.type),
  code: props.code,
  name: props.name
})

</script>
<template>
  <ContentDetailWrap>
    <template #header>
      <ElButton @click="go(-1)">返回</ElButton>
      <!-- <ElButton @click="onTestClick">Test</ElButton> -->
    </template>
    <ElRow :gutter="24">
      <ElCol class="middle-col" :span="colSpan.left">
        <ElTable :data="customizedList" @row-click="onCustomizedClick" :border="true" max-height="800" width="auto" highlight-current-row>
          <ElTableColumn prop="code" label="代码" width="90" />
          <ElTableColumn prop="name" label="名称" />
        </ElTable>
      </ElCol>
      <ElCol class="middle-col" :span="colSpan.middle">
        <ElRow :gutter="24">
          <div style="width: 100%; height: 100%;">
            <!-- <KLinePanel3 :data="historyData" :showParam="showParam" /> -->
            <KLinePanel :param="param" :show-table="true" />
          </div>
        </ElRow>
      </ElCol>
      <ElCol class="middle-col" :span="colSpan.right">
        <ElRow :gutter="24">
          <MarginTable :type="selectType" :code="selectCode" />
        </ElRow>
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
