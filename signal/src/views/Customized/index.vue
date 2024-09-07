<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { apiCreate, apiInfos, apiRemove } from '@/api/customized';
import { InfoModel } from '@/api/customized/types';
import { ElTable, ElTableColumn, ElButton, ElMessageBox, ElSelect, ElOption, ElMessage,
  ElDropdown, ElDropdownMenu, ElDropdownItem, ElRow } from 'element-plus'
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { AListModel, apiAList, apiHistory, HistoryDataModel } from '@/api/data/wrap';

const { push } = useRouter()

type item = {
  info: InfoModel
  data?: HistoryDataModel
}
const codeType = ref<string>('Stock')
const tableData = ref<item[]>([])
const alistData = ref<AListModel[]>([])
// const filterListData = ref<AListModel[]>([])
const selectCode = ref<string>('')
const listHolder = ref<string>('click load button to fetch..')
// const loading = ref(false)


async function fetchHistoryData(code: string, type: number): Promise<HistoryDataModel | undefined> {
  const ret = await apiHistory({
    code: code
  }, type)

  if (ret.result.length > 0) {
    return ret.result[0]
  }
  return undefined
}

async function fetchInfos() {
  const ret = await apiInfos({})
  tableData.value = []
  for (const item of ret.result) {
    tableData.value.push({
      info: item,
      data: await fetchHistoryData(item.code, item.type)
    })
  }
}

async function onCreateClick() {
  const ret = await apiCreate({
    type: (codeType.value == 'Index' ? 0 : 1),
    code: selectCode.value
  })
  if (ret.code == 0) {
    ElMessage({
      type: 'success',
      message: `${selectCode.value} added successfully.`
    })
    await fetchInfos()
  }
}

function onRowClick(row: any) {
  push(`/customized/summary?type=${row.info.type}&code=${row.info.code}&name=${row.info.name}`)
}

async function onDelete(info: InfoModel) {
  const ret = await ElMessageBox.confirm(
    `remove '${info.name}' ?`,
    'Information', 
    {
      confirmButtonText: 'Yes',
      cancelButtonText: 'No',
      type: 'info'
    }
  )  
  if (ret == 'confirm') {
    await apiRemove({id: info.id})
    await fetchInfos()
  }
}

async function fetchAList() {
  listHolder.value = 'loading..'
  const ret = await apiAList((codeType.value == 'Index' ? 0 : 1))
  alistData.value = ret.result
  listHolder.value = 'please choose code..'
}

onMounted(async () => {
  await fetchInfos()
  // await fetchAList()
})

function onCodeTypeCommand(cmd: string) {
  codeType.value = cmd
}

</script>
<template>
  <ContentWrap title="Customized">
    <ElRow>
      <ElDropdown trigger="click" style="padding-right: 8px;" @command="onCodeTypeCommand">
        <ElButton>{{ codeType }}</ElButton>
        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem command="Stock">Stock</ElDropdownItem>
            <ElDropdownItem command="Index">Index</ElDropdownItem>
          </ElDropdownMenu>
        </template>
      </ElDropdown>      
      <ElSelect v-model="selectCode" :disabled="alistData.length==0" filterable clearable :placeholder="listHolder" style="width: 240px;">
        <ElOption v-for="i in alistData" :key="i.code" :value="i.code" :label="`${i.code} ${i.name}`" />
      </ElSelect>
      <ElButton class="btn" @click="fetchAList">Load</ElButton>
      <ElButton class="btn" type="primary" :disabled="selectCode===''" @click="onCreateClick">Add</ElButton>
    </ElRow>
    <ElRow>
      <ElTable :data="tableData" :stripe="true" :border="true" style="width: 100%; margin-top: 12px;" @row-click="onRowClick">
        <!-- <ElTableColumn type="selection" fixed width="50" /> -->
        <ElTableColumn prop="info.code" label="代码" width="80">
          <template #default="{row}">
            <el-button link>
              {{ row.info.code }}
            </el-button>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="info.name" label="名称" width="90" />
        <ElTableColumn prop="data.price" label="现价" width="80" />
        <ElTableColumn prop="data.percentage" label="涨跌幅%" width="90" />
        <ElTableColumn prop="data.amount" label="涨跌额" width="80" />
        <ElTableColumn prop="data.volatility" label="振幅%" width="80" />          
        <ElTableColumn prop="data.open" label="今开" width="80" />
        <ElTableColumn prop="data.close" label="昨收" width="80" />
        <ElTableColumn prop="data.high" label="最高" width="80" />
        <ElTableColumn prop="data.low" label="最低" width="80" />
        <ElTableColumn prop="data.volume" label="成交量" width="120" />
        <ElTableColumn prop="data.turnover" label="成交额" width="140" />
        <ElTableColumn prop="data.rate" label="换手率%" width="90" />
        <ElTableColumn prop="data.date" label="行情日期" width="120" />
        <ElTableColumn prop="info.updated" label="添加日期" width="120">
          <template #default="{row}">
            {{ row.info.updated.slice(0, 10) }}
          </template>
        </ElTableColumn>
        <ElTableColumn fixed="right" label="操作" min-width="100">
          <template #default="{row}">   
            <ElButton link type="danger" @click.stop="onDelete(row.info)">删除</ElButton>
          </template>
        </ElTableColumn>      
      </ElTable>
    </ElRow>
  </ContentWrap>
</template>
<style lang="css">
.btn {
  margin-left: 12px;
}
</style>
