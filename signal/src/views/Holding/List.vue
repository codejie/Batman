<template>
  <ContentWrap title="Holding">
    <ElRow>
      <ElCol :span="24">
        <ElCard>
          <ElTable :data=data :stripe="true" :border="true">
            <ElTableColumn prop="id" label="ID" width="50"></ElTableColumn>
            <ElTableColumn prop="type" label="Type" width="50"></ElTableColumn>
            <ElTableColumn prop="code" label="Code" width="100"></ElTableColumn>
            <ElTableColumn prop="name" label="Name" width="100"></ElTableColumn>
            <ElTableColumn prop="flag" label="Flag" width="50"></ElTableColumn>
            <ElTableColumn prop="created" label="Created" width="100"></ElTableColumn>
            <ElTableColumn prop="updated" label="Updated" width="100"></ElTableColumn>
            <ElTableColumn prop="quantity" label="Quantity" width="100"></ElTableColumn>
            <ElTableColumn prop="expense" label="Expense" width="100"></ElTableColumn>
            <ElTableColumn prop="price_avg" label="Price Avg" width="100"></ElTableColumn>
            <ElTableColumn prop="price_cur" label="Price Cur" width="100"></ElTableColumn>
            <ElTableColumn prop="revenue" label="Revenue" width="100"></ElTableColumn>
            <ElTableColumn prop="profit" label="Profit" width="100"></ElTableColumn>
            <ElTableColumn prop="profit_percent" label="Profit %" width="100"></ElTableColumn>
          </ElTable>
        </ElCard>
      </ElCol>
    </ElRow>
  </ContentWrap>
</template>

<script lang="ts">
interface HoldingData {
  id: number
  type: number
  code: string
  name: string
  flag: number
  created: Date
  updated: Date
  quantity: number
  expense: number

  price_avg: number
  price_cur?: number
  revenue?: number // price_cur * quantity
  profit?: number // revenue - expense
  profit_percent?: number
}
</script>

<script setup lang="ts">
import { apiHistory } from '@/api/data'
import { apiRecord } from '@/api/holding'
import { ContentWrap } from '@/components/ContentWrap'
import { onMounted, ref } from 'vue'

const data = ref<HoldingData[]>([])

onMounted(() => {
  fetch()
})

async function fetch() {
  const ret = await apiRecord({})
  for (const item of ret.result) {
    const ret_current = await apiHistory({
      type: item.type,
      code: item.code
    })
    const current = ret_current.result[0]
    data.value.push({
      id: item.id,
      type: item.type,
      code: item.code,
      name: item.name,
      flag: item.flag,
      created: item.created,
      updated: item.updated,
      quantity: item.quantity,
      expense: item.expense,
      price_avg: item.expense / item.quantity,
      price_cur: current.price,
      revenue: current.price * item.quantity,
      profit: current.price * item.quantity - item.expense,
      profit_percent: (current.price * item.quantity - item.expense) / item.expense
    })
  }
}

</script>
