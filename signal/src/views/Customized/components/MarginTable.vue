<script setup lang="ts">
import { watch } from 'vue';

const props = defineProps({
  code: {
    type: String,
    required: true
  },
  days: {
    type: Number,
    required: false,
    default: () => 5
  }
})

watch(
  () => props.code,
  () => {
    console.log(`${props.code} changed`)
  }
)

</script>
<template>
  {{ code }}
</template>
<style lang="css">
</style>
