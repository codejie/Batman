<script setup lang="ts">
import { apiInfos } from '@/api/algorithm'
import { AlgorithmModel, ArgumentModel, InfosRequest } from '@/api/algorithm/types'
import { onMounted, ref } from 'vue'
import { ElTable, ElTableColumn, ElInput, ElSelect, ElOption } from 'element-plus'

const props = defineProps({
  name: {
    type: String
  }
})
// const props = defineProps(['name'])
const algorithm = ref<AlgorithmModel>()

const data = ref<
  {
    arg: ArgumentModel
    value: any
  }[]
>([])

defineExpose({
  name: props.name,
  data
})

onMounted(async () => {
  const ret = await apiInfos({
    name: props.name
  } as InfosRequest)
  algorithm.value = ret.result as AlgorithmModel
  algorithm.value.args?.forEach((item) => {
    data.value.push({
      arg: item,
      value: item.default || undefined
    })
  })
})
</script>
<template>
  <b>{{ algorithm?.name }}: {{ algorithm?.desc }}</b>
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
    <ElTableColumn prop="arg.desc" label="Description" width="300" />
  </ElTable>
</template>
