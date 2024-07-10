<script setup lang="ts">
import { PropType, defineProps } from 'vue'
import { InstanceModel } from '@/api/strategy/types'

const props = defineProps({
  instance: {
    type: Object as PropType<InstanceModel>
  }
})
</script>
<template>
  <div>
    {{ instance?.name }}
  </div>
</template>
