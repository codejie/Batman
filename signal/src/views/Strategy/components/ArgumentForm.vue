<script setup lang="ts">
import { ArgumentModel } from '@/api/strategy/types'
import { ElTable, ElTableColumn, ElInput } from 'element-plus'
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
  values: data.value
})
// watch(
//   () => props.args,
//   (value) => {
//     console.log(value)
//     data.value = []
//     value?.forEach((item) => {
//       data.value.push({
//         arg: item,
//         value: undefined
//       })
//     })
//   }
// )

onMounted(() => {
  console.log(props.args)
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
  <div>{{ data }}</div>
  <ElTable :data="data" border style="width: 100%">
    <ElTableColumn prop="arg.name" label="Name" width="100" />
    <ElTableColumn prop="arg.unit" label="Unit" width="100" />
    <ElTableColumn label="Value" width="120">
      <template #default="scope">
        {{ scope.row.arg.type }}
        <div v-if="scope.row.arg.type != 'option'">
          <ElInput />
        </div>
        <div v-else>
          {{ 'abc' }}
        </div>
      </template>
    </ElTableColumn>
    <ElTableColumn prop="value" label="Value" width="100" />
    <ElTableColumn prop="arg.desc" label="Desc" width="200" />
  </ElTable>
</template>
