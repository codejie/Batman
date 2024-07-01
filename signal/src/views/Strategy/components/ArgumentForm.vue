<script setup lang="ts">
import { ArgumentModel } from '@/api/strategy/types'
import { ElTable, ElTableColumn, ElInput, ElSelect, ElOption } from 'element-plus'
import { PropType, onMounted, ref } from 'vue'

const data = ref<
  {
    arg: ArgumentModel
    value: any
  }[]
>([])

const props = defineProps({
  args: {
    type: Array as PropType<ArgumentModel[]>
  }
})

defineExpose({
  data
})

onMounted(() => {
  data.value = []
  props.args?.forEach((item) => {
    data.value.push({
      arg: item,
      value: item.default || null
    })
  })
})
</script>
<template>
  <!-- <div>{{ data }}</div> -->
  <ElTable :data="data" border style="width: 100%">
    <ElTableColumn prop="arg.name" label="Name" width="120" />
    <ElTableColumn prop="arg.unit" label="Unit" width="100" />
    <ElTableColumn label="Value" width="220">
      <template #default="scope">
        <div v-if="scope.row.arg.type != 'option'">
          <ElInput v-model="scope.row.value" />
        </div>
        <div v-else>
          <ElSelect v-model="scope.row.value">
            <ElOption
              v-for="item in scope.row.arg.value"
              :key="item.value"
              :label="item.desc"
              :value="item.value"
            />
          </ElSelect>
        </div>
      </template>
    </ElTableColumn>
    <!-- <ElTableColumn prop="value" label="Value" width="100" /> -->
    <ElTableColumn prop="arg.desc" label="Description" width="300" />
  </ElTable>
</template>
