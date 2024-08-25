<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { ElRow, ElCol, ElButton, ElTable, ElTableColumn, ElDropdown, ElDropdownMenu, ElDropdownItem, ElInput, ElText } from 'element-plus'
import { KLineChart4 } from '@/components/KLine'
import { ref, unref, watch } from 'vue';
import { apiHistory, apiInfo } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';

type CodeItem = {
  type?: number
  code: string
  name?: string
}

const chart = ref(null)
const codeType = ref<string>('Stock')
const codeList = ref<CodeItem[]>([])
const inputCode = ref<string>()
const itemCode = ref<CodeItem>()
const itemHistoryData = ref<HistoryDataModel>()
const itemTitleOutput = ref<string>()
const itemDataOutput = ref<string>()

let searchTimer: NodeJS.Timeout
watch(
  () => inputCode.value,
  async () => {
    clearTimeout(searchTimer)
    searchTimer = setTimeout(async () => {
        itemTitleOutput.value = ''
        itemDataOutput.value = ''
        
        const ret = await apiInfo({
        code: inputCode.value!
      })
      if (ret.result) {
        itemCode.value = {
          type: codeType.value == 'Stock' ? 1 : 0,
          code: ret.result.code,
          name: ret.result.name
        }
        itemTitleOutput.value = `${unref(itemCode)?.code}(${unref(itemCode)?.name}):  ` 
      }
    }, 1000)
  }
)

watch(
  () => itemCode.value,
  async () => {
      const ret = await apiHistory({
      code: itemCode.value!.code
    })

    if (ret.result.length > 0) {
      itemHistoryData.value = ret.result[0]
      itemDataOutput.value = makeItemData()
    } 
  }
)

function makeItemData() {
  return `${unref(itemHistoryData)?.date}\
  | 现价:${unref(itemHistoryData)?.price}\
  | 涨跌幅:${unref(itemHistoryData)?.percentage}%\
  | 涨跌额:${unref(itemHistoryData)?.amount}\
  | 振幅:${unref(itemHistoryData)?.volatility}%\
  | 今开:${unref(itemHistoryData)?.open}\
  | 昨收:${unref(itemHistoryData)?.close}\
  | 最高:${unref(itemHistoryData)?.high}\
  | 最低:${unref(itemHistoryData)?.low}\
  | 成交量:${unref(itemHistoryData)?.volume}\
  | 成交额:${unref(itemHistoryData)?.turnover}\
  | 换手率:${unref(itemHistoryData)?.rate}%`
}

function onCodeTypeCommand(cmd: string) {
  codeType.value = cmd
}

function onCodeListClick(row: CodeItem) {

}

</script>
<template>
  <ContentWrap title="Lookup">
    <ElRow class="row" :gutter="24">
      <ElCol :span="24">
        <ElDropdown trigger="click" @command="onCodeTypeCommand">
          <ElButton>{{ codeType }}</ElButton>
          <template #dropdown>
            <ElDropdownMenu>
              <ElDropdownItem command="Stock">Stock</ElDropdownItem>
              <ElDropdownItem command="Index">Index</ElDropdownItem>
            </ElDropdownMenu>
          </template>
        </ElDropdown>
        <ElInput v-model="inputCode" style="width: 80px;" max-length="6"/>
        <ElButton type="primary">TEST</ElButton>
        <ElText tag="b" size="default">{{ itemTitleOutput }}</ElText>
        <ElText size="default">{{ itemDataOutput }}</ElText>
      </ElCol>
    </ElRow>
    <ElRow class="row" :gutter="24">
      <ElCol :span="3">
        <ElTable :data="codeList" size="small" @row-click="onCodeListClick" :border="true" max-height="800" width="auto" highlight-current-row>
          <ElTableColumn prop="code" label="Code" />
          <ElTableColumn prop="name" label="Name" />
          <ElTableColumn label="Action" />
        </ElTable>
      </ElCol>
      <ElCol :span="21">
        <ElRow class="row" :gutter="24">
          <div>aaa</div>
        </ElRow>
        <KLineChart4 class="row" ref="chart" />
      </ElCol>
    </ElRow>
  </ContentWrap>
</template>
<style lang="css">
.row {
  padding: 4px;
  outline: 1px solid gray;
}
</style>
