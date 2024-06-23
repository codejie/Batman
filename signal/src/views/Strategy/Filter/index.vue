<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { Table, TableColumn } from '@/components/Table'
import { useTable } from '@/hooks/web/useTable'
import { apiList, apiRemove } from '@/api/strategy'
import { PropType, ref, unref } from 'vue'
import { ElTable, ElTableColumn } from 'element-plus'

defineOptions({
  name: 'Filter'
})

const { t } = useI18n()
const { push } = useRouter()

const listInstance = [
  {
    id: '0',
    name: 'name'
  }
]

const onCreate = () => {
  push('/strategy/filter/create')
}
</script>

<template>
  <ContentWrap>
    <div class="mb-10px">
      <BaseButton type="primary" @click="onCreate">{{ t('common.create') }}</BaseButton>
    </div>
    <ElTable :data="listInstance" border style="width: 100%">
      <ElTableColumn prop="id" label="ID" width="100" />
      <ElTableColumn prop="name" label="Name" width="180" />
    </ElTable>
  </ContentWrap>
</template>
