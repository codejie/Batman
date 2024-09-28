<script setup lang="ts">
import { formatToDate } from '@/utils/dateUtil';
import { ref } from 'vue';


const date = ref<string>()

date.value = formatToDate('2024-09-22T16:00:00.000Z', 'YYYY-MM-DD HH:MM:ss')

</script>
<template>
  <ContentWrap title="Test">
    {{ date }}
    <!-- <div>
      <ElButton @click="onTestClick">Test</ElButton>
      <ElButton @click="onTest1Click">Test1</ElButton>
      <ElButton @click="onTest2Click">Test2</ElButton>
      <ElButton @click="onTest3Click">Test3</ElButton>
      <ElButton @click="onTest4Click">Test4</ElButton>
    </div> -->
    <!-- <KLinePanel :param="param" :show-table="true" /> -->
    <!-- <KLineChart4 ref="klc3" /> -->
      <!-- <KLinePanel2 :req-param="param" /> -->
    <!-- <Echart :options="options" /> -->
  </ContentWrap>
</template>