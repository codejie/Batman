<script setup lang="ts">
import type { ArgumentItem } from '@/api/calc'

defineProps<{
  argumentList: ArgumentItem[]
}>()
</script>

<template>
  <div class="argument-display">
    <h4>Calculation Arguments</h4>
    <ul>
      <li v-for="arg in argumentList" :key="arg.id">
        <pre>{{ arg.arguments }}</pre>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.argument-display {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 4px;
}
h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}
pre {
  background-color: #f5f5f5;
  padding: 0.5rem;
  border-radius: 4px;
}
</style>
