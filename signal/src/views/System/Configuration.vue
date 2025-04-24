<script setup lang="ts">
import { apiDbExport, urlDbImport } from '@/api/system';
import { ContentWrap } from '@/components/ContentWrap'
import { ElButton, ElDivider, ElUpload, ElRow, ElCol, UploadInstance } from 'element-plus'
import { ref } from 'vue';

const uploadRef = ref<UploadInstance>()
const showSubmit = ref(false)

async function onExport() {
  const ret = await apiDbExport({});
  console.log('ret', ret);
}

function onUploadChange() {
  showSubmit.value = true
}

function onUploadRemove() {
  showSubmit.value = false
}

</script>

<template>
  <ContentWrap title="系统配置">
    <ElDivider content-position="left">数据导出导入</ElDivider>
    <div  class="ma-12px" >
      <ElRow :gutter="24">
        <ElCol :span="2">
          <ElButton type="primary" @click="onExport">导出</ElButton>
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
              <ElButton type="primary">导入..</ElButton>
            </template>
            <ElButton class="ml-12px" v-if="showSubmit" type="danger" @click="uploadRef?.submit()">提交</ElButton>
          </ElUpload>
        </ElCol>
        <ElCol :span="18" />
      </ElRow>
    </div>
  </ContentWrap>
</template>
