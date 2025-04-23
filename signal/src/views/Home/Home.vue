<script setup lang="ts">
import { apiDbExport } from '@/api/system';
import { ContentWrap } from '@/components/ContentWrap'
import { ElButton } from 'element-plus'

async function onTest() {
  const ret = await apiDbExport({});
  console.log('ret', ret);
}

</script>

<template>
  <ContentWrap title="Home">
    <ElButton type="primary" @click="onTest">Test</ElButton>

  </ContentWrap>
</template>
