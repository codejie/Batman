<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { apiList, apiRemove } from '@/api/strategy'
import { PropType, onMounted, ref, unref } from 'vue'
import { ElTable, ElTableColumn } from 'element-plus'

defineOptions({
  name: 'Filter'
})

const { t } = useI18n()
const { push } = useRouter()

const listInstance = ref<any[]>([])

const fetchInstanceList = async () => {
  const ret = await apiList({})
  for (const i of ret.result) {
    listInstance.value.push(i)
  }
}

onMounted(() => {
  fetchInstanceList()
})

const onBtnCreate = () => {
  push('/strategy/filter/create')
}
</script>

<template>
  <ContentWrap title="Filter Strategy Instance">
    <div class="mb-10px">
      <BaseButton type="primary" @click="onBtnCreate">{{ t('common.create') }}</BaseButton>
    </div>
    <ElTable :data="unref(listInstance)" border style="width: 100%">
      <ElTableColumn prop="id" label="ID" width="100" />
      <ElTableColumn prop="name" label="Name" width="180" />
      <ElTableColumn prop="strategy" label="Strategy" width="200" />
    </ElTable>
  </ContentWrap>
</template>
