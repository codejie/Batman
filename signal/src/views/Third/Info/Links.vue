<script lang="ts">
export const options = reactive({
  type: undefined as number | undefined,
  code: undefined as string | undefined,
  name: undefined as string | undefined,
  collapse: false as boolean,
  target: undefined as string | undefined
})
type LinkInfo = {
  title: string,
  url: string,
  tooltip?: string,
}
</script>
<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap';
import { reactive, ref, watch } from 'vue';
import { ElButton, ElInput, ElRow, ElCol } from 'element-plus';
import { DArrowLeft, DArrowRight } from '@element-plus/icons-vue'
import { TYPE_STOCK } from '@/api/data';
import Navigator from './components/Navigator.vue';

const props = defineProps({
  type: {
    type: Number,
    required: false,
    default: TYPE_STOCK
  },
  code : {
    type: String,
    required: false
  },
  name: {
    type: String,
    required: false,
    default: undefined
  }
})

const collapse = ref<boolean>(false)
const url = ref<string | undefined>()

watch(
  () => collapse.value,
  (newVal) => {
    options.collapse = newVal
  },
  { immediate: true }
)

watch(
  () => options.target,
  (newVal) => {
    url.value = newVal
  },
  { immediate: true }
)

watch(
  () => props.code,
  (newVal) => {
    options.code = newVal
  },
  { immediate: true }
)

</script>
<template>
  <ContentWrap>
    <ElRow :gutter="24">
      <ElCol :span="3">
        <ElInput :placeholder="'请输入股票代码'" v-model="options.code" />
      </ElCol>
      <ElCol :span="1">
        <ElButton :disabled="true">查询</ElButton>
      </ElCol>
      <ElCol :span="20"></ElCol>
    </ElRow>
    <ElRow :gutter="24" class="tac" style="margin-top: 10px;">
      <ElCol :span="collapse ? 1 : 3">
        <ElButton type="info" :icon="collapse ? DArrowRight : DArrowLeft" @click="collapse = !collapse" />
        <Navigator />
      </ElCol>
      <ElCol :span="collapse ? 23 : 21">
        <iframe :src="url" width="100%" height="800px" frameborder="0"></iframe>
      </ElCol>
    </ElRow>
  </ContentWrap>
</template>
