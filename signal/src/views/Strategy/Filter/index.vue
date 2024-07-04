<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { apiList } from '@/api/strategy'
import { onMounted, ref, unref } from 'vue'
import { ElTable, ElTableColumn, ElButton } from 'element-plus'
// import { useEmitt } from '@/hooks/event/useEmitt'

// defineOptions({
//   name: 'Filter'
// })

const { t } = useI18n()
const { push } = useRouter()
// const { emitter } = useEmitt()

// useEmitt({
//   name: 'back',
//   callback: () => {
//     console.log('back.....')
//   }
// })

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

function onDetail(id: string) {
  console.log(id)
}
</script>

<template>
  <ContentWrap title="Filter Strategy Instance">
    <div class="mb-10px">
      <BaseButton type="primary" @click="onBtnCreate">{{ t('common.create') }}</BaseButton>
    </div>
    <ElTable :data="unref(listInstance)" border style="width: 100%">
      <ElTableColumn prop="name" label="Name" width="180" />
      <ElTableColumn prop="state" label="State" width="80" />
      <ElTableColumn prop="strategy" label="Strategy" width="200" />
      <ElTableColumn prop="id" label="ID" width="200" />
      <ElTableColumn fixed="right" label="Operations" min-width="120">
        <template #default="scope">
          <ElButton link type="primary" size="small" @click="onDetail(scope.row.id)"
            >Detail</ElButton
          >
          <ElButton link type="primary" size="small">Delete</ElButton>
        </template>
      </ElTableColumn>
    </ElTable>
  </ContentWrap>
</template>
