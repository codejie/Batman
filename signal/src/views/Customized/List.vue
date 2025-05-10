<script lang="ts">
interface CreateForm {
  type: string
  code: string
}

interface Item {
  record: RecordsItem
  calc?: CustomizedCalcItem
}
</script>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { ElDialog, ElText, ElForm, ElFormItem, ElInput, ElButton, ElTable, ElTableColumn, ElMessageBox, ElSelect, ElOption } from 'element-plus'
import { apiCreate, apiRecords, RecordsItem, apiRemove } from '@/api/customized';
import { apiGetLatestHistoryData, apiGetSpotData, TYPE_INDEX, TYPE_STOCK } from '@/api/data';
import { ContentWrap } from '@/components/ContentWrap';
import { calcCustomizedData, CustomizedCalcItem } from '@/calc/customized';
import { formatToDateTime } from '@/utils/dateUtil'
import { KLineDialog } from '@/components/KLine'

const createDialogVisible = ref<boolean>(false)
const createForm = ref<CreateForm>({
  type: '股票',
  code: ''
})
const data = ref<Item[]>([])
const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<any>({})

async function fetch() {
  const ret = await apiRecords({})
  data.value = []

  const stocks = ret.result.filter(item => item.type === TYPE_STOCK).map(item => item)
  const indexes = ret.result.filter(item => item.type === TYPE_INDEX).map(item => item)

  if (stocks.length > 0) {
    const codes: string[] = stocks.map(item => item.code)
    const stockRet = await apiGetSpotData({ type: TYPE_STOCK, codes: codes })
    for (const item of stocks) {
      const spot = stockRet.result.find(i => i.代码 === item.code)
      data.value.push({
        record: item,
        calc: calcCustomizedData(spot)
      })
    }
  }

  if (indexes.length > 0) {
    const codes: string[] = indexes.map(item => item.code)
    const indexRet = await apiGetSpotData({ type: TYPE_INDEX, codes: codes })
    for (const item of indexes) {
      const spot = indexRet.result.find(i => i.代码 === item.code)
      data.value.push({
        record: item,
        calc: calcCustomizedData(spot)
      })
    }
  }


  // for (const item of ret.result) {
  //   const history = await apiGetLatestHistoryData({ type: item.type, code: item.code })
  //   data.value.push({
  //     record: item,
  //     calc: calcCustomizedData(history.result)
  //   })
  // }
}

async function onAdd() {
  await apiCreate({
    type: createForm.value.type == '股票' ? TYPE_STOCK : TYPE_INDEX,
    code: createForm.value.code
  })
  createDialogVisible.value = false
  await fetch()
}

async function onRemove(id: number) {
  const confirm = await ElMessageBox.confirm(
    '是否确认删除?',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
  if (confirm) {
    await apiRemove({
      id: id
    })
    await fetch()
  }  
}

function onRecordClick(row: HoldingRecordItem) {
  reqParam.value = {
    code: row.code,
    name: row.name,
    type: row.type,
  //   start: row.record.created,
  //   end: new Date()
  }
  klineDialogVisible.value = true
}

onMounted(async () => {
  await fetch()
})
</script>

<template>
  <ContentWrap>
    <div>
      <ElButton class="my-4" type="primary" @click="createDialogVisible=true">增加自选</ElButton>    
    </div>
    <div>
      <ElTable :data="data" :border="true" stripe :default-sort="{ prop: 'record.updated', order: 'descending' }">
        <ElTableColumn type="index" width="40" />
        <ElTableColumn prop="record.holding" label="持有" width="60">
          <template #default="{ row }">
            {{ (row.record.holding ? '是' : '否') }}
          </template>
        </ElTableColumn>
        <!-- <ElTableColumn prop="record.code" label="代码" width="100">
          <template #default="{ row }">
              <ElText tag="b" @click="onRecordClick(row.record)">{{ row.record.code }}</ElText>
            </template>
        </ElTableColumn>
        <ElTableColumn prop="record.name" label="名称" min-width="100" /> -->
        <ElTableColumn prop="record.code" label="名称/代码" min-width="60">
          <template #header>
            <ElText>名称/代码</ElText>
          </template>
          <template #default="{ row }">
            <div @click="onRecordClick(row.record)">
              <div><ElText tag="b">{{ row.record.name }}</ElText></div>
              <div><ElText tag="b">{{ row.record.code }}</ElText></div>
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="type" label="类型" min-width="100">
          <template #default="{ row }">
            {{ row.record.type == TYPE_STOCK ? '股票' : '指数' }}
          </template>
        </ElTableColumn>
        <ElTableColumn label="现价/日期" min-width="100">
            <template #default="{ row }">
              {{ `${row.calc?.price.toFixed(2)} / ${row.calc?.date.substring(5)}` }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="calc.price_change" label="涨跌额" min-width="100" />
        <ElTableColumn prop="calc.price_change_rate" label="涨跌幅" min-width="100" />
        <ElTableColumn label="操作时间" prop="record.updated" min-width="100">
          <template #default="{ row }">
            {{ formatToDateTime(row.record.updated) }}
          </template>
        </ElTableColumn>        
        <ElTableColumn prop="action" label="操作" min-width="100">
          <template #default="{row}">
            <ElButton type="danger" @click="onRemove(row.record.id)">删除</ElButton>
          </template>
        </ElTableColumn>
      </ElTable>
    </div>
    <ElDialog v-model="createDialogVisible" :destroy-on-close="true" width="25%">
      <template #header>
        <ElText tag="b">新增持股记录</ElText>
      </template>
      <template #default>
        <ElForm :model="createForm" label-position="right" label-width="auto">
          <ElFormItem label="类型">
            <ElSelect v-model="createForm.type">
              <ElOption label="股票" value="股票" />
              <ElOption label="指数" value="指数" />
            </ElSelect>
          </ElFormItem>
          <ElFormItem label="代码">
            <ElInput v-model="createForm.code" :maxlength="6" />
          </ElFormItem>
        </ElForm>
      </template>
      <template #footer>
        <ElButton @click="createDialogVisible=false">取消</ElButton>
        <ElButton type="primary" @click="onAdd">确定</ElButton>
      </template>      
    </ElDialog>
    <KLineDialog :visible="klineDialogVisible" :req-param="reqParam" @update:on-close="klineDialogVisible = false" width="60%" />    
  </ContentWrap>    
</template>
