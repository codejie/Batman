<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { apiList, apiRemove } from '@/api/strategy'
import { onMounted, ref, unref } from 'vue'
import { ElTable, ElTableColumn, ElButton, ElMessageBox, ElMessage } from 'element-plus'
import { InstanceModel } from '@/api/strategy/types'
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

const listInstance = ref<InstanceModel[]>([])

const fetchInstanceList = async () => {
  listInstance.value = []
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

function makeState(instance: InstanceModel): string {
  if (instance.is_remove) {
    return 'Removed'
  }
  switch(instance.state) {
    case 0:
      return 'Init'
    case 1:
      return 'Ready'
    case 2:
      return 'Executed'
    case 3:
      return 'Error'
    case 4:
      return 'Missed'
    case 5:
      return 'Removed'
    case 6:
      return 'Paused'
    default:
      return 'Unknown'
  }
}

async function onDelete(id: string) {
  const ret = await ElMessageBox.confirm(
    `delete strategy instance '${id}'?`,
    'Warning', 
    {
      confirmButtonText: 'Yes',
      cancelButtonText: 'No',
      type: 'warning'
    }
  )
  if (ret === 'confirm') {
    const r = await apiRemove({
      id: id
    })
    if (r.code == 0) {
      ElMessage({
        type: 'success',
        message: 'strategy instance be deleted.'
      })
    } else {
      ElMessage({
        type: 'error',
        message: 'delete strategy instance failed.'
      })
    }
    await fetchInstanceList()
  }
}
</script>

<template>
  <ContentWrap title="Filter Strategy Instance">
    <div class="mb-10px">
      <BaseButton type="primary" @click="onBtnCreate">{{ t('common.create') }}</BaseButton>
    </div>
    <ElTable :data="unref(listInstance)" border style="width: 100%">
      <ElTableColumn prop="name" label="Name" width="180" />
      <ElTableColumn prop="state" label="State" width="100">
        <template #default="scope">
          {{ makeState(scope.row) }}
        </template>
      </ElTableColumn>
      <ElTableColumn prop="strategy" label="Strategy" width="200" />
      <ElTableColumn prop="id" label="ID" width="200" />
      <ElTableColumn fixed="right" label="Operations" min-width="120">
        <template #default="scope">
          <ElButton link type="primary" size="small" @click="onDetail(scope.row.id)">Detail</ElButton>
          <ElButton link type="primary" size="small" @click="onDelete(scope.row.id)">Delete</ElButton>
        </template>
      </ElTableColumn>
    </ElTable>
  </ContentWrap>
</template>
