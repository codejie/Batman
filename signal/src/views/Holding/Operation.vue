<script lang="ts">
interface OperationData {
  id: number
  holding: number
  action: number
  quantity: number
  price: number
  expense: number
  comment?: string
  created: Date
}

interface HoldingOperationData {
  holdingData: HoldingData
  items: OperationData[]
}

</script>
<script setup lang="ts">
import { ElButton, ElRow, ElTable, ElTableColumn } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref } from 'vue';
import { getHoldingData, HoldingData, viewOptions } from './List.vue';
import { apiOperationList } from '@/api/holding';

const newDialogVisible = ref<boolean>(false)
const data = ref<HoldingOperationData[]>([])

onMounted(async () => {
  const holding = await getHoldingData(viewOptions.selected)
  for (const item of holding) {
    data.value.push({
      holdingData: item,
      items: []
    })
  }

  const ret = await apiOperationList({
    holding: viewOptions.selected
  })

  for (const item of ret.result) {
    const holding = data.value.find((x) => x.holdingData.id === item.holding)
    holding!.items.push(item)
  }
})

</script>

<template>
  <ContentWrap title="Operation">
    <ElRow :gutter="24">
      <ElButton class="my-4 ml-4" type="primary" @click="newDialogVisible=true">增加</ElButton>
    </ElRow>
    <ElRow :gutter="24">
      <ElTable :data="data" stripe :border="true">
        <ElTableColumn type="index" width="40" />
        <ElTableColumn type="expand">
          <template #default="{ row }">
            <div class="mx-24px my-8px">
              <h4>操作记录({{ row.items.length }})</h4>
            </div>
            <div class="mx-24px my-8px">       
              <ElTable size="small" :data="row.items" stripe :border="true">
                <ElTableColumn type="index" width="40" />
                <ElTableColumn label="数量" prop="quantity" />
                <ElTableColumn label="价格" prop="price" />
                <ElTableColumn label="费用" prop="expense" />
                <ElTableColumn label="备注" prop="comment" />
                <ElTableColumn label="创建时间" prop="created" />
              </ElTable>
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn label="代码" prop="holdingData.code" />
        <ElTableColumn label="名称" prop="holdingData.name" />
        <ElTableColumn label="数量" prop="holdingData.quantity" />
        <ElTableColumn label="成本" prop="holdingData.expense" />
        <ElTableColumn label="当前价" prop="holdingData.price_cur" />
        <ElTableColumn label="收益" prop="holdingData.revenue" />
        <ElTableColumn label="利润" prop="holdingData.profit" />
        <ElTableColumn label="利润率" prop="holdingData.profit_percent" />
        <ElTableColumn label="创建时间" prop="holdingData.created" />
        <ElTableColumn label="更新时间" prop="holdingData.updated" />
      </ElTable>
    </ElRow>

  </ContentWrap>
</template>

