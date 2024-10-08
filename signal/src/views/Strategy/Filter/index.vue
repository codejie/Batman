<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { useRouter } from 'vue-router'
import { apiList, apiRemove, apiReset } from '@/api/strategy'
import { onMounted, ref, unref } from 'vue'
import { ElTable, ElTableColumn, ElButton, ElMessageBox, ElMessage, ElDialog } from 'element-plus'
import { InstanceListItemModel } from '@/api/strategy/types'
import DetailForm from './components/DetailForm.vue'
import ResultForm from './components/ResultForm.vue'

const { push } = useRouter()

const detailDialogVisible = ref(false)
const resultDialogVisible = ref(false)

const selectInstance = ref<InstanceListItemModel>()
const listInstance = ref<InstanceListItemModel[]>([])

const fetchInstanceList = async () => {
  listInstance.value = []
  const ret = await apiList({})
  listInstance.value = ret.result
}

onMounted(async () => {
  await fetchInstanceList()
})

const onBtnCreate = () => {
  push('/strategy/filter/create')
}

function onDetail(row: any) {
  selectInstance.value = row
  detailDialogVisible.value = true
}

function onResult(row: any) {
  selectInstance.value = row
  resultDialogVisible.value = true
}

function makeState(instance: InstanceListItemModel): string {
  if (instance.is_removed) {
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

function makeUpdated(str: string): string {
  if (str) {
    const date = new Date(str)
    return `${date.toISOString().slice(0, 10)} ${date.toISOString().slice(11, 19)}` // `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`
  } else {
    return '-'
  }
}

function makeResult(instance: InstanceListItemModel): string {
  const results = instance.results
  if (!results) {
    return '-'
  }
  return `${results}`
}

async function onDelete(id: string) {
  const ret = await ElMessageBox.confirm(
    `delete strategy instance '${id}'?`,
    'Warning', 
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
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

async function onReset(id: string, name: string) {
  const ret = await ElMessageBox.confirm(
    `reset strategy instance '${name}'?`,
    'Information', 
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    }
  )
  if (ret === 'confirm') {
    const r = await apiReset({
      id: id
    })
    if (r.code == 0) {
      ElMessage({
        type: 'success',
        message: 'strategy instance be reseted.'
      })
    } else {
      ElMessage({
        type: 'error',
        message: 'reset strategy instance failed.'
      })
    }
    await fetchInstanceList()
  }
}
</script>

<template>
  <ContentWrap title="选股策略">
    <div class="mb-10px">
      <!-- <BaseButton type="primary" @click="onBtnCreate">{{ t('common.create') }}</BaseButton> -->
      <ElButton type="primary" @click="onBtnCreate">创建</ElButton>
    </div>
    <ElTable :data="unref(listInstance)" :border="true" style="width: 100%">
      <ElTableColumn prop="name" label="名称" width="180" />
      <ElTableColumn prop="state" label="状态" width="100">
        <template #default="scope">
          {{ makeState(scope.row) }}
        </template>
      </ElTableColumn>
      <ElTableColumn prop="strategy" label="策略" width="200" />
      <ElTableColumn label="命中" width="60">
        <template #default="scope">
          <ElButton link type="primary" @click="onResult(scope.row)">
            {{ makeResult(scope.row) }}
          </ElButton> 
        </template>
      </ElTableColumn>
      <ElTableColumn prop="latest_updated" label="更新时间" width="200">
        <template #default="scope">
          {{ makeUpdated(scope.row.latest_updated) }}
        </template>
      </ElTableColumn>
      <ElTableColumn prop="id" label="ID" width="200" />
      <ElTableColumn fixed="right" label="操作" min-width="120">
        <template #default="scope">
          <ElButton link type="primary" @click="onDetail(scope.row)">详情</ElButton>
          <ElButton link type="info" :disabled="scope.row.is_removed == false" @click="onReset(scope.row.id, scope.row.name)">重置</ElButton>          
          <ElButton link type="danger" @click="onDelete(scope.row.id)">删除</ElButton>
        </template>
      </ElTableColumn>
    </ElTable>
    <ElDialog v-model="detailDialogVisible" :title="`${selectInstance?.name}(${selectInstance?.id})`" width="50%" destroy-on-close>
      <DetailForm :instance-id="selectInstance!.id" />
      <template #footer>
        <ElButton type="primary" @click="detailDialogVisible=false">关闭</ElButton>
      </template>
    </ElDialog>
    <ElDialog v-model="resultDialogVisible" :title="`${selectInstance?.name}(${selectInstance?.id})`" width="65%" destroy-on-close>
      <ResultForm :instance-id="selectInstance!.id" />
      <template #footer>
        <ElButton type="primary" @click="resultDialogVisible=false">关闭</ElButton>
      </template>
    </ElDialog>
  </ContentWrap>
</template>
