<script setup lang="ts">
import ContentWrap from '@/components/ContentWrap/src/ContentWrap.vue';
import { ElRow, ElText, ElTable, ElTableColumn } from 'element-plus';


</script>
<template>
  <ContentWrap title="持仓列表">
    <ElRow :gutter="24">
      <ElText>abc</ElText>
      Summary
    </ElRow>
    <ElRow :gutter="24">
      <ElTable>
        <ElTableColumn type="index" />
      </ElTable>
    </ElRow>
  </ContentWrap>
</template>
