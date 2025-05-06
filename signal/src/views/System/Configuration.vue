<script setup lang="ts">
import { apiDownloadList, TYPE_STOCK, TYPE_INDEX } from '@/api/data';
import { apiDbExport, apiDbRemoveAllHistoryData, urlDbImport } from '@/api/system';
import { ContentWrap } from '@/components/ContentWrap'
import { ElButton, ElDivider, ElUpload, ElRow, ElCol, UploadInstance, ElMessage, ElMessageBox } from 'element-plus'
import { ref } from 'vue';

const uploadRef = ref<UploadInstance>()
const showSubmit = ref(false)

async function onExport() {
  const ret = await apiDbExport({});
}

async function onImport() {
  const retConfirm = await ElMessageBox.confirm('是否提交数据?', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
  if (retConfirm === "confirm") {
    uploadRef.value?.submit()
    uploadRef.value?.clearFiles()

    showSubmit.value = false
  }
}
function onUploadChange() {
  showSubmit.value = true
}

function onUploadRemove() {
  showSubmit.value = false
}

async function onDownloadList(type: number) {
  const retConfirm = await ElMessageBox.confirm('是否更新列表信息?', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
  if (retConfirm === "confirm") {
    const ret = await apiDownloadList({
      type: type
    })
    if (ret.code == 0) {
      ElMessage.success('更新成功.')
    } else {
      ElMessage.error('更新失败.')
    }
  }
}

async function onHistoryDelete() {
  const retConfirm = await ElMessageBox.confirm('是否清除所有历史数据?', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
  if (retConfirm === "confirm") {
    const ret = await apiDbRemoveAllHistoryData({})
    if (ret.code == 0) {
      ElMessage.success('清除成功.')
    } else {
      ElMessage.error('清除失败.')
    }
  }
}
</script>

<template>
  <ContentWrap title="系统配置">
    <ElDivider content-position="left">导出导入</ElDivider>
    <div  class="ma-12px" >
      <ElRow :gutter="24">
        <ElCol :span="2">
          <ElButton type="primary" @click="onExport">持仓数据导出</ElButton>
        </ElCol>
        <ElCol :span="4">
          <ElUpload
            ref="uploadRef"
            :action=urlDbImport
            :multiple="false"
            :auto-upload="false"
            :on-change="onUploadChange"
            :on-remove="onUploadRemove"
          >
            <template #trigger>
              <ElButton type="primary">持仓数据导入..</ElButton>
            </template>
            <ElButton class="ml-12px" v-if="showSubmit" type="danger" @click="onImport">提交</ElButton>
          </ElUpload>
        </ElCol>
        <ElCol :span="18" />
      </ElRow>
    </div>
    <ElDivider content-position="left">数据更新</ElDivider>
    <div  class="ma-12px" >
      <ElRow :gutter="24">
        <ElCol :span="2">
          <ElButton type="primary" @click="onDownloadList(TYPE_STOCK)">股票列表信息</ElButton>
        </ElCol>
        <ElCol :span="2">
          <ElButton type="primary" @click="onDownloadList(TYPE_INDEX)">指数列表信息</ElButton>
        </ElCol>        
      </ElRow>
    </div>
    <ElDivider content-position="left">数据清除</ElDivider>
    <div  class="ma-12px" >
      <ElRow :gutter="24">
        <ElCol :span="2">
          <ElButton type="primary" @click="onHistoryDelete()">清除历史数据</ElButton>
        </ElCol>
        <!-- <ElCol :span="2">
          <ElButton type="primary" @click="onDownloadList(TYPE_INDEX)">指数列表信息</ElButton>
        </ElCol>         -->
      </ElRow>
    </div>    
  </ContentWrap>
</template>
