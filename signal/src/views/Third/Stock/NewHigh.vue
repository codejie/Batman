<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import NewHighTable from './components/NewHighTable.vue';
import { ElRow, ElCol } from 'element-plus';
</script>
<template>
  <ContentWrap title="创新高">
    <ElRow :gutter="24">
      <ElCol :span="12">
        <ElRow>
          <NewHighTable name="历史新高" :category="3" />
        </ElRow>
        <ElRow>
          <NewHighTable name="半年新高" :category="1" />
        </ElRow>
      </ElCol>
      <ElCol :span="12">
        <ElRow>
          <NewHighTable name="一年新高" :category="2" />
        </ElRow>
        <ElRow>
          <NewHighTable name="月创新高" :category="0" />
        </ElRow>
      </ElCol>      
    </ElRow>
  </ContentWrap>
</template>
