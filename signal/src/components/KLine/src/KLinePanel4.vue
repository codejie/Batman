<script setup lang="ts">
import { ref } from 'vue';
import { ElRow, ElCol } from 'element-plus';
import { DataParam, ShowParam } from '..';

const props = defineProps({
  code: {
    type: String,
    required: true
  }
})

const showParam = ref<ShowParam>({
  maLines: [9, 12, 26 ],
  hideVolume: false,
  markLines: true  
})

const dataParam = ref<DataParam>({
  code: props.code
})

</script>
<template>
  <ElRow :gutter="24">
    {{ code }}
  </ElRow>
  <ElRow :gutter="24">
    <KLinePanel :dataParam="dataParam" :showParam="showParam" />    
  </ElRow>
</template>
<style lang="css">
</style>
