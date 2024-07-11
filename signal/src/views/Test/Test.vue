<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { Echart, EChartsOption } from '@/components/Echart'

const barOptions: EChartsOption = {
  title: [
    {
      text: 'analysis.weeklyUserActivity',
      left: 'center'
    },
    {
      text: 'analysis.weeklyUserActivity',
      left: 'left',
      backgroundColor: 'rgba(0, 0, 0, 0.15)'
    }    
  ]
}
</script>
<template>
  <ContentWrap title="Test">
    <div>
      <Echart :options="barOptions" :height="300" />
    </div>
  </ContentWrap>
</template>