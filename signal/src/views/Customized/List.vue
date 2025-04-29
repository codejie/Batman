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
import { ElDialog, ElText, ElForm, ElFormItem, ElInput, ElButton, ElTable, ElTableColumn, ElMessageBox } from 'element-plus'
import { apiCreate, apiRecords, RecordsItem, apiRemove } from '@/api/customized';
import { apiGetLatestHistoryData, TYPE_INDEX, TYPE_STOCK } from '@/api/data';
import { ContentWrap } from '@/components/ContentWrap';
import { calcCustomizedData, CustomizedCalcItem } from '@/calc/customized';
import { formatToDateTime } from '@/utils/dateUtil'
import { KLineDialog } from '@/components/KLine'
import { HoldingRecordItem } from '@/api/holding';

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

  for (const item of ret.result) {
    const history = await apiGetLatestHistoryData({ type: item.type, code: item.code })
    data.value.push({
      record: item,
      calc: calcCustomizedData(history.result)
    })
  }
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

function onKLineDialogClose() {
  klineDialogVisible.value = false
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
      <ElTable :data="data" :border="true" stripe>
        <ElTableColumn type="index" width="40" />
        <ElTableColumn prop="record.holding" label="持有" width="60">
          <template #default="{ row }">
            {{ (row.record.holding ? '是' : '否') }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="record.code" label="代码" width="100">
          <template #default="{ row }">
              <ElText tag="b" @click="onRecordClick(row.record)">{{ row.record.code }}</ElText>
            </template>
        </ElTableColumn>
        <ElTableColumn prop="record.name" label="名称" width="200" />
        <!-- <ElTableColumn prop="type" label="类型" width="100" /> -->
        <ElTableColumn label="现价/日期" min-width="60">
            <template #default="{ row }">
              {{ `${row.calc?.price.toFixed(2)} / ${row.calc?.date.substring(5)}` }}
            </template>
          </ElTableColumn>
          <ElTableColumn prop="calc.price_change" label="涨跌额" width="100" />
        <ElTableColumn prop="calc.price_change_rate" label="涨跌幅" width="100" />
        <ElTableColumn label="操作时间" prop="record.updated" min-width="120">
          <template #default="{ row }">
            {{ formatToDateTime(row.record.updated) }}
          </template>
        </ElTableColumn>        
        <ElTableColumn prop="action" label="操作" width="100">
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
            <ElInput v-model="createForm.type" :disabled="true" />
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
    <KLineDialog :visible="klineDialogVisible" :req-param="reqParam" :title="reqParam?.name" @update:on-close="onKLineDialogClose" width="60%" />    
  </ContentWrap>    
</template>
