<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import NewHighTable from './components/NewHighTable.vue'
import { ElTabs, ElTabPane } from 'element-plus'
import { ref } from 'vue'

const activeName = ref('first')
</script>
<template>
  <ContentWrap title="创新高">
    <ElTabs v-model="activeName" style="height: auto">
      <ElTabPane label="历史新高" name="first">
        <NewHighTable name="历史新高" :category="3" />
      </ElTabPane>
      <ElTabPane label="半年新高" name="second">
        <NewHighTable name="半年新高" :category="1" />
      </ElTabPane>
      <ElTabPane label="一年新高" name="third">
        <NewHighTable name="一年新高" :category="2" />
      </ElTabPane>
      <ElTabPane label="月创新高" name="forth">
        <NewHighTable name="月创新高" :category="0" />
      </ElTabPane>
    </ElTabs>
    <!-- <ElRow :gutter="24">
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
    </ElRow> -->
  </ContentWrap>
</template>
