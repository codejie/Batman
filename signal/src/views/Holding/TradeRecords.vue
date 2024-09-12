<script setup lang="ts">
import ContentWrap from '@/components/ContentWrap/src/ContentWrap.vue';
import { ElRow, ElText, ElTable, ElTableColumn } from 'element-plus';


</script>
<template>
  <ContentWrap title="交易记录">
    <ElRow :gutter="24">
      <ElText>abc</ElText>
    </ElRow>
    <ElRow :gutter="24">
      <ElTable>
        <ElTableColumn type="index" />
      </ElTable>
    </ElRow>
  </ContentWrap>
</template>
