<script lang="ts">
interface OperationData {
  id: number
  type: number
  code: string
  name: string
  flag: number
  created: Date
  updated: Date
  quantity: number
  expense: number

  price_avg: number | string
  price_cur?: number
  revenue?: number | string// price_cur * quantity
  profit?: number | string// revenue - expense
  profit_percent?: number | string
}

type CurrentData = {
  [key in string]: {
    name: string
    price?: number
  }
}
</script>
<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref } from 'vue';
import { viewOptions } from './List.vue';
import { apiOperationList } from '@/api/holding';
import { getTypeCodeString } from '@/utils/comm';

const newDialogVisible = ref<boolean>(false)
const data = ref<OperationData[]>([])
const currentData = ref<CurrentData>({})

onMounted(async () => {
  if (viewOptions.selected) {
    currentData.value[getTypeCodeString(
      viewOptions.selected.type,
      viewOptions.selected.code
    )] = {
      name: viewOptions.selected.name,
      price: viewOptions.selected.price_cur
    }
  }

  const ret = await apiOperationList({
    holding: viewOptions.selected ? viewOptions.selected.id : undefined
  })



})

</script>

<template>
  <ContentWrap title="Operation">
    <ElRow :gutter="24">
      <ElButton class="my-4 ml-4" type="primary" @click="newDialogVisible=true">增加</ElButton>
    </ElRow>
    <ElRow :gutter="24">
      <ElTable :data="data" :stripe="true" :border="true">
        <ElTableColumn type="index" width="40"></ElTableColumn>
        <ElTableColumn label="操作" width="100">
          <template #default="{ row }">
            <ElButton type="text" @click="onOperation(row)">操作</ElButton>
          </template>
        </ElTableColumn>
      </ElTable>
    </ElRow>

  </ContentWrap>
</template>

