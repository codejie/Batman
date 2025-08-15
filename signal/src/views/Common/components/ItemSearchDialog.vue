<script lang="ts">
interface ViewForm {
  type: string
  title: string
  code: string
}
</script>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { ElDialog, ElText, ElForm, ElFormItem, ElInput, ElButton, ElSelect, ElOption, ElMessage } from 'element-plus'
import { apiGetItemInfo, TYPE_INDEX, TYPE_STOCK, apiGetName } from '@/api/data';

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'confirm'])

const viewDialogVisible = ref(props.visible)
watch(() => props.visible, (val) => {
  viewDialogVisible.value = val
})
watch(viewDialogVisible, (val) => {
  if (!val) {
    emit('update:visible', false)
  }
})


const viewForm = ref<ViewForm>({
  type: '股票',
  title: '',
  code: ''
})

function onSearchChanged() {
  viewForm.value.code = ''
}

async function searchItem(key: string) {
  if (key) {
    const type = viewForm.value.type == '股票' ? TYPE_STOCK : TYPE_INDEX
    const ret = await apiGetItemInfo({
      type: type,
      key: key
    })
    if (ret.result) {
      viewForm.value.title = `${ret.result.name}/${ret.result.code}`
      viewForm.value.code = ret.result.code
    } else {
      ElMessage.warning('Not Found')
    }
  }
}

async function onConfirm() {
  const type = viewForm.value.type == '股票' ? TYPE_STOCK : TYPE_INDEX
  const ret = await apiGetName({
    type: type,
    code: viewForm.value.code
  })
  
  if (ret.result) {
    emit('confirm', {
      code: viewForm.value.code,
      name: ret.result,
      type: type,
    })
  } else {
    ElMessage.error('Failed to get name')
  }
  emit('update:visible', false)
}

function onCancel() {
    emit('update:visible', false)
}

</script>

<template>
    <ElDialog v-model="viewDialogVisible" :destroy-on-close="true" width="25%">
      <template #header>
        <ElText tag="b">快速查看</ElText>
      </template>
      <template #default>
        <ElForm :model="viewForm" label-position="right" label-width="auto">
          <ElFormItem label="类型">
            <ElSelect v-model="viewForm.type" @change="onSearchChanged">
              <ElOption label="股票" value="股票" />
              <ElOption label="指数" value="指数" />
            </ElSelect>
          </ElFormItem>
          <ElFormItem label="名称/代码">
            <ElInput v-model="viewForm.title" placeholder="请输入代码或名称" :maxlength="6" @change="onSearchChanged">
              <template #append>
                <ElButton :disabled="viewForm.title === ''" @click="searchItem(viewForm.title)">搜索</ElButton>
              </template>
            </ElInput>
          </ElFormItem>
        </ElForm>
      </template>
      <template #footer>
        <ElButton @click="onCancel">取消</ElButton>
        <ElButton type="primary" :disabled="viewForm.code === ''" @click="onConfirm">确定</ElButton>
      </template>
    </ElDialog>
</template>
