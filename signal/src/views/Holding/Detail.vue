<script setup lang="ts">
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProfitTraceData, getTraceData } from '@/calc/holding'
import { apiGetHistoryData } from '@/api/data'
import { TYPE_STOCK } from '@/api/data/types'

const { go } = useRouter()

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  }
})

const holding = computed(() => Number(props.id))

onMounted(async () => {
  const ret = await getTraceData(holding.value)
  console.log('ret', ret)
})

async function onTest() {
  const ret = await apiGetHistoryData({
    type: TYPE_STOCK,
    code: '000006',
  })
  console.log('ret', ret)
  const profit = await getProfitTraceData(TYPE_STOCK, '000006', holding.value)
  console.log('profit', profit)
}

</script>

<template>
  <ContentDetailWrap title="Operation">
    <template #header>
      <BaseButton type="primary" @click="go(-1)">返回</BaseButton>
      <BaseButton type="primary" @click="onTest">Test</BaseButton>
    </template>    
  </ContentDetailWrap>
</template>

